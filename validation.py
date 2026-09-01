def energy_balance_error(row, heat):
    """Compare heat lost by the hot stream with heat gained by the cold stream."""

    # Energy balance for the hot stream.
    heat_lost = row["hot_flow_kg_s"] * row["hot_cp_J_kgK"] * (
        row["hot_inlet_C"] - heat["hot_out_C"]
    )

    # Energy balance for the cold stream.
    heat_gained = row["cold_flow_kg_s"] * row["cold_cp_J_kgK"] * (
        heat["cold_out_C"] - row["cold_inlet_C"]
    )

    # A value near zero means the two energy balances agree.
    return abs(heat_lost - heat_gained)


def mass_balance_error(row, mass):
    """Check that inlet solute equals outlet solute plus transferred solute."""

    # Solute flow entering and leaving with the source stream.
    inlet_rate = row["source_flow_m3_s"] * row["solute_in_mol_m3"]
    outlet_rate = row["source_flow_m3_s"] * mass["solute_out_mol_m3"]

    # A value near zero means inlet = outlet + transferred solute.
    return abs(inlet_rate - outlet_rate - mass["mass_transfer_mol_s"])
