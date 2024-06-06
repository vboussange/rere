import os
import requests
import zipfile
import shutil
import matplotlib.pyplot as plt

# Set up results directory
results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../results/"))

# Set up project folder
os.makedirs(os.path.join(os.path.dirname(__file__), "../../data/own"), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), "../../data/foreign"), exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# Download data
weather_fl = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/own/weather.dat"))
if not os.path.isfile(weather_fl):
    weather_url = "https://raw.githubusercontent.com/mauro3/CORDS/master/data/weather.dat"
    info_url = "https://raw.githubusercontent.com/mauro3/CORDS/master/data/weather.info"
    weather_info_fl = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/own/weather.info"))
    print("Downloading weather data...")
    response = requests.get(weather_url)
    with open(weather_fl, 'wb') as f:
        f.write(response.content)
    response = requests.get(info_url)
    with open(weather_info_fl, 'wb') as f:
        f.write(response.content)

dem_fl = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/foreign/dhm200.asc"))
if not os.path.isfile(dem_fl):
    dem_url = "https://data.geo.admin.ch/ch.swisstopo.digitales-hoehenmodell_25/data.zip"
    zip_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/foreign/dhm200.zip"))
    print("Downloading DEM data...")
    response = requests.get(dem_url)
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    # Extract specific file from zip
    print("Extracting DEM data...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if "DHM200.asc" in file:
                with zip_ref.open(file) as src, open(dem_fl, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
    # Remove zip file
    os.remove(zip_path)

mask_fl = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/own/glacier_mask.asc"))
if not os.path.isfile(mask_fl):
    mask_url = "https://raw.githubusercontent.com/mauro3/CORDS/master/data/glacier_mask.asc"
    print("Downloading glacier mask data...")
    response = requests.get(mask_url)
    with open(mask_fl, 'wb') as f:
        f.write(response.content)

# Read data and visualize it (Placeholder for future implementation)

# Run melt model for a point at 2600m (Placeholder for future implementation)

# Run melt model for the whole glacier (Placeholder for future implementation)

# Example usage of matplotlib for visualization
def plot_example():
    # Placeholder for actual data
    plt.figure()
    plt.plot([0, 1, 2, 3], [0, 1, 4, 9])
    plt.title("Example Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.savefig(os.path.join(results_dir, "example_plot.png"))
    plt.show()

if __name__ == "__main__":
    plot_example()
