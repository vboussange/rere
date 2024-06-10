import numpy as np
import matplotlib.pyplot as plt
import os
from src.data import read_campbell
from src.utils import make_sha_filename
from src.glacier_mass_balance import glacier_net_balance_fn
import pandas as pd
import rioxarray

def read_data(weather_fl, dem_fl, mask_fl, Ps0):
    t, Ts, Ps, z_weather_station = read_campbell(weather_fl)
    dem = rioxarray.open_rasterio(dem_fl, mask_and_scale=True)
    mask = rioxarray.open_rasterio(mask_fl, mask_and_scale=True)
    Ps = Ps0 + Ts * 0  # Make precipitation a vector of the same length as Ts
    return t, Ts, dem, mask, Ps, z_weather_station

def visualize_data(t, Ts, mask, dem, results_dir):
    plt.plot(t, Ts)
    plt.xlabel("time (d)")
    plt.ylabel("T (C)")
    plt.savefig(make_sha_filename(os.path.join(results_dir, "breithorn_T"), ".png"))
    plt.close()

    mask.plot()
    plt.savefig(make_sha_filename(os.path.join(results_dir, "breithorn_mask"), ".png"))
    plt.close()

    dem.plot()
    plt.savefig(make_sha_filename(os.path.join(results_dir, "breithorn_dem"), ".png"))
    plt.close()

def run_model_for_glacier(dem, mask, Ts, Ps, melt_factor, T_threshold, lapse_rate, z_weather_station, results_dir):
    zs = dem.where(mask == 1).to_dataframe(name="z").dropna() - z_weather_station
    dt = np.diff(t)[0]
    
    # Placeholder function for glacier_net_balance_fn
    glacier_net_balance, net_balance = glacier_net_balance_fn(zs["z"], dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
    
    net_balance_df = zs.copy()
    net_balance_df["net_balance"] = net_balance
    net_balance_map = net_balance_df.to_xarray()["z"].sortby("x", "y")
    
    net_balance_map.plot()
    plt.savefig(make_sha_filename(os.path.join(results_dir, "breithorn_net_balance_field"), ".png"))
    plt.close()
    
    return zs, dt

def generate_output_table(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate, results_dir):
    output_data = []
    for dT in range(-4, 5):
        Ts_offset = Ts + dT
        massbalance_, _ = glacier_net_balance_fn(zs, dt, Ts_offset, Ps, melt_factor, T_threshold, lapse_rate)
        output_data.append([dT, massbalance_])
    
    output_csv_path = make_sha_filename(os.path.join(results_dir, "deltaT_impact"), ".csv")
    pd.DataFrame(output_data, columns=["Temperature Offset", "Mass Balance"]).to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    PARAMS = {"lapse_rate": -0.6/100,
                "melt_factor": 0.005,
                "T_threshold": 4}
    
    results_dir = "../results/"
    
    # Define file paths and constants
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../teaching_material/data/workshop-reproducible-research"))
    weather_fl = os.path.join(data_dir, "own", "weather.dat")
    mask_fl = os.path.join(data_dir, "own", "mask_breithorngletscher","mask_breithorngletscher.asc")
    dem_fl = os.path.join(data_dir, "foreign", "swisstopo_dhm200_cropped", "dhm200_cropped.asc")
    Ps0 = 0.005  # Mean (and constant) precipitation rate [m/d]
    
    # Read data
    t, Ts, dem, mask, Ps, z_weather_station = read_data(weather_fl, dem_fl, mask_fl, Ps0)
    
    # Visualize data
    visualize_data(t, Ts, mask, dem, data_dir)
    
    # Run model for the whole glacier
    zs, dt = run_model_for_glacier(dem, mask, Ts, Ps, PARAMS["melt_factor"], PARAMS["T_threshold"], PARAMS["lapse_rate"], z_weather_station, results_dir)
    
    # Generate output table
    generate_output_table(zs["z"], dt, Ts, Ps, PARAMS["melt_factor"], PARAMS["T_threshold"], PARAMS["lapse_rate"], results_dir)
