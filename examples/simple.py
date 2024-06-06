import numpy as np
import matplotlib.pyplot as plt
import os
from src.glacier_mass_balance import melt, total_point_balance, total_glacier_balance, lapse
from src.utils import make_sha_filename

# Define synthetic functions

def synthetic_T(t):
    """
    Generate synthetic temperature for a given time `t`.
    
    Args:
        t (np.ndarray): The time.
    
    Returns:
        np.ndarray: The synthetic temperature.
    """
    return -10 * np.cos(2 * np.pi / 364 * t) - 8 * np.cos(2 * np.pi * t) + 5

def synthetic_P(t):
    """
    Generate synthetic precipitation
    
    Args:
        t (np.ndarray): The time.
    
    Returns:
        np.ndarray: The synthetic precipitation.
    """
    return np.full(t.shape, 8e-3)

def synthetic_glacier():
    """
    Generate synthetic glacier elevation.
    
    Returns:
        np.ndarray: Array of elevations.
    """
    x = np.arange(0, 5500, 500)
    elevation = x * 0.2 + 1400
    return elevation

# Constants
lapse_rate = -0.6 / 100
melt_factor = 0.005
T_threshold = 4
dt = 1 / 24
t = np.arange(0, 365 + dt, dt)

# Plot the synthetic weather
plt.figure()
plt.plot(t, synthetic_T(t))
plt.xlabel("time (d)")
plt.ylabel("T (°C)")
results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../results"))
os.makedirs(results_dir, exist_ok=True)
plt.savefig(make_sha_filename(os.path.join(results_dir, "synthetic_T"), ".png"))

# Run the model for one year at a point
ele = 1500
Ts_ele = lapse(synthetic_T(t), ele, lapse_rate)
Ps = synthetic_P(t)
point_balance = total_point_balance(dt, Ts_ele, Ps, melt_factor, T_threshold)
print(f"Total point balance at elevation {ele} m: {point_balance}")

# Run the model for one year for the whole glacier
zs = synthetic_glacier()
Ts = synthetic_T(t)
smb = total_glacier_balance(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate)
print(f"Total glacier balance: {smb}")

# Generate output table
output_data = []
for dT in range(-4, 5):
    Ts_offset = synthetic_T(t) + dT
    smb_offset = total_glacier_balance(zs, dt, Ts_offset, Ps, melt_factor, T_threshold, lapse_rate)
    output_data.append([dT, smb_offset])

# Save output to CSV
import csv
output_csv_path = make_sha_filename(os.path.join(results_dir, "deltaT_impact"), ".csv")
with open(output_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Temperature Offset', 'Surface Mass Balance'])
    csvwriter.writerows(output_data)

print(f"Output saved to {output_csv_path}")
