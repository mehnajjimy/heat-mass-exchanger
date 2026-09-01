# Code Notes

## Whole program

```text
input file
   -> main.py
   -> heat_transfer.py and mass_transfer.py
   -> validation.py
   -> io_utils.py
   -> output files
```

Run `python3 main.py` from the `heat-mass-exchanger` folder. Paths such as
`outputs/results.csv` start from that folder.

## `main.py`

```python
import pandas as pd
```

Loads pandas. Pandas turns lists and spreadsheet data into tables called
DataFrames.

```python
from heat_transfer import heat_exchange
from io_utils import read_cases, save_results
from mass_transfer import mass_exchange
from validation import energy_balance_error, mass_balance_error
```

Brings the functions from the other Python files into `main.py` so they can be
used here.

```python
INPUT_FILE = "inputs/cases.csv"
```

Chooses the input file. Change `.csv` to `.xlsx` to use the included Excel file.

```python
cases = read_cases(INPUT_FILE)
results = []
```

`read_cases` loads the input spreadsheet into a pandas table. `results` starts
as an empty list. One finished result will be added for every input row.

```python
for _, row in cases.iterrows():
```

Starts a loop. Each trip through the loop handles one exchanger case. `row`
contains the values from that spreadsheet row. The underscore means the row
number is not needed.

```python
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
```

Takes the heat-related values from the current input row and sends them to
`heat_exchange`. The returned answers are stored in the `heat` dictionary.

```python
mass = mass_exchange(
    row["solute_in_mol_m3"],
    row["mass_K_m_s"],
    row["mass_area_m2"],
    row["source_flow_m3_s"],
)
```

Takes the mass-transfer values from the same row and sends them to
`mass_exchange`. The returned answers are stored in the `mass` dictionary.

```python
results.append(
    {
        "case_id": row["case_id"],
        **heat,
        **mass,
        "energy_balance_error_W": energy_balance_error(row, heat),
        "mass_balance_error_mol_s": mass_balance_error(row, mass),
    }
)
```

Builds one result row and adds it to the `results` list.

- `case_id` keeps the name of the input case.
- `**heat` adds every heat answer to the row.
- `**mass` adds every mass-transfer answer.
- the last two lines calculate the balance errors.

```python
save_results(pd.DataFrame(results))
```

`pd.DataFrame(results)` turns the list of result dictionaries into a table.
`save_results` then saves that table here:

```text
outputs/results.csv
outputs/results.xlsx
```

```python
print("simulation complete")
print("results saved in outputs/")
```

Prints a short message so the user knows the program finished.

## `heat_transfer.py`

```python
import math
```

Loads Python's math tools. This model needs the exponential function.

```python
def heat_exchange(t_hot, t_cold, m_hot, m_cold, cp_hot, cp_cold, u, area):
```

Creates the heat calculation function. The names inside the parentheses are the
values the function receives from `main.py`.

```python
c_hot = m_hot * cp_hot
c_cold = m_cold * cp_cold
c_min = min(c_hot, c_cold)
c_max = max(c_hot, c_cold)
```

Calculates each stream's heat-capacity rate and identifies the smaller and
larger rates.

```python
capacity_ratio = c_min / c_max
ntu = u * area / c_min
```

Calculates the heat-capacity ratio and the heat-transfer NTU.

```python
if abs(capacity_ratio - 1) < 1e-10:
    effectiveness = ntu / (1 + ntu)
else:
    exponent = math.exp(-ntu * (1 - capacity_ratio))
    effectiveness = (1 - exponent) / (1 - capacity_ratio * exponent)
```

Calculates counter-current exchanger effectiveness. The first equation handles
the special case where both heat-capacity rates are equal. The `else` equation
handles all other cases.

```python
maximum_heat_duty = c_min * (t_hot - t_cold)
heat_duty = effectiveness * maximum_heat_duty
hot_out = t_hot - heat_duty / c_hot
cold_out = t_cold + heat_duty / c_cold
```

Calculates the maximum possible heat duty, the actual heat duty, and both outlet
temperatures.

```python
return {
    "heat_duty_W": heat_duty,
    "effectiveness": effectiveness,
    "NTU_heat": ntu,
    "hot_out_C": hot_out,
    "cold_out_C": cold_out,
}
```

Returns the answers as a dictionary. The quoted names become output column
headers.

## `mass_transfer.py`

```python
import math
```

Loads the exponential function used by the membrane equation.

```python
def mass_exchange(c_in, k, area, flow):
```

Creates the mass-transfer function and lists the four values it needs.

```python
ntu = k * area / flow
c_out = c_in * math.exp(-ntu)
transfer_rate = flow * (c_in - c_out)
removal_fraction = 1 - c_out / c_in
```

Calculates mass-transfer NTU, outlet concentration, transferred amount per
second, and the fraction removed.

```python
return {
    "solute_out_mol_m3": c_out,
    "mass_transfer_mol_s": transfer_rate,
    "mass_effectiveness": removal_fraction,
    "NTU_mass": ntu,
}
```

Returns the mass-transfer answers. The quoted names become output columns.

## `validation.py`

```python
heat_lost = ...
heat_gained = ...
return abs(heat_lost - heat_gained)
```

Uses the two stream energy balances. A result near zero means heat lost by the
hot stream equals heat gained by the cold stream.

```python
inlet_rate = ...
outlet_rate = ...
return abs(inlet_rate - outlet_rate - mass["mass_transfer_mol_s"])
```

Checks the solute balance. A result near zero means inlet solute equals outlet
solute plus transferred solute.

## `io_utils.py`

```python
from pathlib import Path
import pandas as pd
from openpyxl.utils import get_column_letter
```

Loads tools for folders, tables, Excel files, and Excel column letters.

```python
def read_cases(path):
    if path.endswith(".csv"):
        return pd.read_csv(path)
    if path.endswith(".xlsx"):
        return pd.read_excel(path)
    raise ValueError("input file must be .csv or .xlsx")
```

Reads CSV when the filename ends in `.csv`, reads Excel when it ends in
`.xlsx`, and gives a clear error for any other file type.

```python
def format_sheet(worksheet, data):
    worksheet.freeze_panes = "A2"
    for number, column in enumerate(data.columns, start=1):
        worksheet.column_dimensions[get_column_letter(number)].width = min(
            max(len(column) + 2, 14), 30
        )
```

Freezes the header row and makes each Excel column wide enough to read. The
`min` and `max` keep widths between 14 and 30.

```python
Path("outputs").mkdir(exist_ok=True)
data.to_csv("outputs/results.csv", index=False)
```

Creates the `outputs` folder if it does not exist, then saves the result table as
CSV. `index=False` prevents pandas from adding an unwanted row-number column.

```python
with pd.ExcelWriter("outputs/results.xlsx", engine="openpyxl") as writer:
    data.to_excel(writer, sheet_name="results", index=False)
    format_sheet(writer.sheets["results"], data)
```

Opens an Excel writer, saves the same table in a sheet named `results`, formats
the sheet, and closes the file when the block finishes.
