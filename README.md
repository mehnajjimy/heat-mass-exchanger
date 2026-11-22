# Heat and Mass Exchanger

This program reads exchanger cases, calculates heat and mass transfer, checks
the balances, and saves the answers.

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
