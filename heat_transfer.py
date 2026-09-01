import math


def heat_exchange(t_hot, t_cold, m_hot, m_cold, cp_hot, cp_cold, u, area):
    """Calculate heat duty and outlet temperatures with the NTU method."""

    # Heat-capacity rate tells us how much heat each stream can carry per degree.
    c_hot = m_hot * cp_hot
    c_cold = m_cold * cp_cold

    # The NTU equations use the smaller and larger heat-capacity rates.
    c_min = min(c_hot, c_cold)
    c_max = max(c_hot, c_cold)

    # Calculate the two values used by the counter-current effectiveness equation.
    capacity_ratio = c_min / c_max
    ntu = u * area / c_min

    # Equal heat-capacity rates need a special equation to avoid division by zero.
    if abs(capacity_ratio - 1) < 1e-10:
        effectiveness = ntu / (1 + ntu)
    else:
        exponent = math.exp(-ntu * (1 - capacity_ratio))
        effectiveness = (1 - exponent) / (1 - capacity_ratio * exponent)

    # Use effectiveness to find heat duty, then use energy balances for outlets.
    maximum_heat_duty = c_min * (t_hot - t_cold)
    heat_duty = effectiveness * maximum_heat_duty
    hot_out = t_hot - heat_duty / c_hot
    cold_out = t_cold + heat_duty / c_cold

    # Return a dictionary. These names become columns in the output files.
    return {
        "heat_duty_W": heat_duty,
        "effectiveness": effectiveness,
        "NTU_heat": ntu,
        "hot_out_C": hot_out,
        "cold_out_C": cold_out,
    }
