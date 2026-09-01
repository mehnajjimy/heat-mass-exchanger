import pandas as pd

from heat_transfer import heat_exchange
from io_utils import read_cases, save_results
from mass_transfer import mass_exchange
from validation import energy_balance_error, mass_balance_error


# Change .csv to .xlsx here when you want to use the Excel input.
INPUT_FILE = "inputs/cases.csv"

# Read every input row and create an empty list for finished result rows.
cases = read_cases(INPUT_FILE)
results = []

# Each input row is one separate exchanger case.
for _, row in cases.iterrows():

    # Send the heat-related columns to the heat model.
    heat = heat_exchange(
        row["hot_inlet_C"],
        row["cold_inlet_C"],
        row["hot_flow_kg_s"],
        row["cold_flow_kg_s"],
        row["hot_cp_J_kgK"],
        row["cold_cp_J_kgK"],
        row["U_W_m2K"],
        row["heat_area_m2"],
    )

    # Send the mass-transfer columns to the membrane model.
    mass = mass_exchange(
        row["solute_in_mol_m3"],
        row["mass_K_m_s"],
        row["mass_area_m2"],
        row["source_flow_m3_s"],
    )

    # Build one output row and add it to the results list.
    results.append(
        {
            "case_id": row["case_id"],
            **heat,  # Add every value returned by heat_exchange.
            **mass,  # Add every value returned by mass_exchange.
            "energy_balance_error_W": energy_balance_error(row, heat),
            "mass_balance_error_mol_s": mass_balance_error(row, mass),
        }
    )

# Turn the result rows into a table, then save results.csv and results.xlsx.
save_results(pd.DataFrame(results))

# Confirm that the program reached the end without an error.
print("simulation complete")
print("results saved in outputs/")
