import numpy as np
import pandas as pd

def read_campbell(file):
    """
    Reads a Campbell logger format file with temperature and precipitation.
    Moves sampling from 30min to 1h.
    
    Args:
        file (str): Path to the file.
    
    Returns:
        tuple: (t, temp, precip, elevation)
        - t: Array of datetime in days since 1.1.2007 0:00.
        - temp: Array of temperatures in degrees Celsius.
        - precip: Array of precipitation in meters per day.
        - elevation: Elevation in meters above sea level (m asl).
    """
    dat = pd.read_csv(file, header=None)
    year, day, HHMM = dat.iloc[:, 1], dat.iloc[:, 2], dat.iloc[:, 3]
    t = parse_campbell_date_time(year, day, HHMM)

    # Adjust sampling rate from 30 min to 1 hour
    t = t[::2]
    temp = dat.iloc[::2, 5].to_numpy()
    precip = (dat.iloc[::2, 6] + dat.iloc[1::2, 6]).to_numpy()  # Summing precipitation
    elevation = 2650

    return t, temp, precip / 1000 * 24, elevation


def parse_campbell_date_time(year, day, HHMM):
    """
    Parse the Campbell logger time format: `year`, `day of year`, `HHMM`.
    
    Args:
        year (int or pd.Series): The year.
        day (int or pd.Series): The day of the year.
        HHMM (int or pd.Series): Time in HHMM format.
    
    Returns:
        np.ndarray: Time in days since 1.1.2007 0:00.
    """
    assert np.all(year == 2007), "Year must be 2007"
    hour = np.floor(HHMM / 100)
    minute = HHMM - 100 * hour
    return day - 1 + hour / 24 + minute / 1440  # 1440 = 24 * 60

if __name__ == "__main__":
    # Test functions
    assert np.isclose(parse_campbell_date_time(2007, 1, 1239), 0.5270833333333333)
    assert np.isclose(parse_campbell_date_time(2007, 365, 2359), 364.9993055555555)
