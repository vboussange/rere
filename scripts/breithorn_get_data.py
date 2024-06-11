"""
this if a very cool script making very cool things and other stuff looooggg texxxxtt hello

"""


import os
import requests
import zipfile
import shutil
from src.utils import download_file, unzip_one_file


def get_data():
    # Directory setup
    results_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../results")
    )
    data_own_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../data/own")
    )
    data_foreign_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../data/foreign")
    )

    os.makedirs(data_own_dir, exist_ok=True)
    os.makedirs(data_foreign_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # Download data
    # Weather data
    weather_url = "https://raw.githubusercontent.com/mauro3/CORDS/master/data/workshop-reproducible-research/own/weather.dat"
    weather_fl = os.path.join(data_own_dir, "weather.dat")
    download_file(weather_url, weather_fl)

    # Glacier mask
    mask_zip_url = "https://github.com/mauro3/CORDS/raw/master/data/workshop-reproducible-research/own/mask_breithorngletscher.zip"
    mask_zip_path = os.path.join(data_own_dir, "mask_breithorngletscher.zip")
    mask_fl = os.path.join(data_own_dir, "mask_breithorngletscher.asc")
    download_file(mask_zip_url, mask_zip_path)
    unzip_one_file(
        mask_zip_path, "mask_breithorngletscher/mask_breithorngletscher.asc", mask_fl
    )

    # Digital Elevation Model (DEM)
    dem_zip_url = "https://github.com/mauro3/CORDS/raw/master/data/workshop-reproducible-research/foreign/swisstopo_dhm200_cropped.zip"
    dem_zip_path = os.path.join(data_foreign_dir, "swisstopo_dhm200_cropped.zip")
    dem_fl = os.path.join(data_foreign_dir, "dhm200_cropped.asc")
    download_file(dem_zip_url, dem_zip_path)
    unzip_one_file(dem_zip_path, "swisstopo_dhm200_cropped/dhm200_cropped.asc", dem_fl)

    # Extra data
    z_weather_station = 2650  # elevation of weather station [m]
    Ps0 = 0.005  # mean (and constant) precipitation rate [m/d]

    print("Data preparation complete.")


if __name__ == "__main__":
    get_data()
