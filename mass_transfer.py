import math


def mass_exchange(c_in, k, area, flow):
    """Calculate membrane mass transfer using a perfect-sink model."""

    # Compare the membrane transfer ability with the source-stream flow rate.
    ntu = k * area / flow

    # The perfect-sink model gives the remaining outlet concentration.
    c_out = c_in * math.exp(-ntu)

    # Calculate how much solute transfers and what fraction is removed.
    transfer_rate = flow * (c_in - c_out)
    removal_fraction = 1 - c_out / c_in

    # Return a dictionary. These names become columns in the output files.
    return {
        "solute_out_mol_m3": c_out,
        "mass_transfer_mol_s": transfer_rate,
        "mass_effectiveness": removal_fraction,
        "NTU_mass": ntu,
    }
