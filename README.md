# Heat and Mass Exchanger

I built a Python simulator that combines a counter-current effectiveness-NTU heat exchanger with a perfect-sink membrane mass-transfer model. It calculates heat duty, outlet temperatures, and solute transfer for each case, then reports energy and solute balance residuals.

The heat model handles the equal heat-capacity-rate limit explicitly. Both supplied cases close the energy and solute balances to floating-point precision. The formulas assume positive stream flow rates and a positive inlet solute concentration.

See the [engineering case study](https://mehnajjimy.com/projects/heat-mass-exchanger/),
[calculation notes](NOTES.md), [sample cases](inputs/cases.csv), and
[sample results](outputs/results.csv).

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Results

The files save inside this project's `outputs` folder:

```text
outputs/results.csv
outputs/results.xlsx
```

CSV is the default input. To use Excel, change `INPUT_FILE` in `main.py` to:

```python
INPUT_FILE = "inputs/cases.xlsx"
```

Short comments beside the Python code explain what each block does.
