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


def net_balance_fn(dt, Ts, Ps, melt_factor, T_threshold):
    """
    Integrate the balance rate (this is at a point) over time for given temperature and precipitation arrays to get the "net balance".

    Args:
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.

    Returns:
        net balance (this is at a point)
    """
    assert len(Ts) == len(Ps)
    total = 0.0
    for T, P in zip(Ts, Ps):
        balance_rate = -melt(T, melt_factor) + accumulate(T, P, T_threshold)
        total += balance_rate * dt
    return total


def glacier_net_balance_fn(zs, dt, Ts, Ps, melt_factor, T_threshold, lapse_rate):
    """
    Calculate:
    - the glacier net balance (integration of balance rate over time and space)
    - the net balance at each point (integration of balance rate over time)

    Args:
        zs: Array of elevations (with the weather station as datum)
        dt: The time step.
        Ts: Array of temperatures.
        Ps: Array of precipitations.
        melt_factor: The factor to compute melt amount.
        T_threshold: The temperature threshold for accumulation.
        lapse_rate: The lapse rate (temperature change per unit elevation change).

    Returns:
        the glacier net balance [m]
        net balance at all points [m]
    """
    glacier_net_balance = 0.0
    net_balance = np.zeros(len(zs))
    for i, z in enumerate(zs):
        TT = [lapse(T, z, lapse_rate) for T in Ts]
        net_balance[i] = net_balance_fn(dt, TT, Ps, melt_factor, T_threshold)
        glacier_net_balance += net_balance[i]
    return glacier_net_balance / len(zs), net_balance

