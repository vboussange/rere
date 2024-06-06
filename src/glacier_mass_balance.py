import numpy as np

def melt(T, melt_factor):
    """
    Calculate the melt amount given temperature `T` and a `melt_factor`.
    
    Args:
        T (float): The temperature.
        melt_factor (float): The factor by which the temperature is scaled to get the melt value.
    
    Returns:
        float: The computed melt amount. Returns 0 if `T` is less than or equal to 0, otherwise returns `T * melt_factor`.
    """
    return max(0.0, T * melt_factor)


def accumulate(T, P, T_threshold):
    """
    Calculate the accumulation given temperature `T`, precipitation `P`, and a temperature threshold `T_threshold`.
    
    Args:
        T (float): The temperature.
        P (float): The precipitation.
        T_threshold (float): The temperature threshold for accumulation.
    
    Returns:
        float: `P` if `T` is less than or equal to `T_threshold`, otherwise returns 0.
    """
    return P if T <= T_threshold else 0.0


def lapse(T, dz, lapse_rate):
    """
    Compute the temperature adjustment using lapse rate for a given elevation change.
    
    Args:
        T (float): The initial temperature.
        dz (float): The change in elevation.
        lapse_rate (float): The lapse rate (temperature change per unit elevation change), note <0
    
    Returns:
        float: The adjusted temperature.
    """
    return T + dz * lapse_rate


def total_point_balance(dt, Ts, Ps, melt_factor, T_threshold):
    """
    Calculate the total point balance over time for given temperature and precipitation arrays.
    
    Args:
        dt (float): The time step.
        Ts (array-like): Array of temperatures.
        Ps (array-like): Array of precipitations.
        melt_factor (float): The factor to compute melt amount.
        T_threshold (float): The temperature threshold for accumulation.
    
    Returns:
        float: The total point balance.
    """
    assert len(Ts) == len(Ps), "Length of temperature and precipitation arrays must be equal."
    total = 0.0
    for T, P in zip(Ts, Ps):
        total -= melt(T, melt_factor) * dt
        total += accumulate(T, P, T_threshold) * dt
    return total


def total_glacier_balance(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate):
    """
    Calculate the total glacier balance over time and elevation.
    
    Args:
        zs (array-like): Array of elevations.
        dt (float): The time step.
        Ts (array-like): Array of temperatures.
        Ps (array-like): Array of precipitations.
        melt_factor (float): The factor to compute melt amount.
        T_threshold (float): The temperature threshold for accumulation.
        lapse_rate (float): The lapse rate (temperature change per unit elevation change).
    
    Returns:
        float: The total glacier balance.
    """
    total = 0.0
    for z in zs:
        adjusted_Ts = [lapse(T, z, lapse_rate) for T in Ts]
        total += total_point_balance(dt, adjusted_Ts, Ps, melt_factor, T_threshold)
    return total
