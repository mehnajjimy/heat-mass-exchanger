# Heat and Mass Exchanger

In the first example, the hot stream entering the modeled exchanger at 90 °C leaves at 63.0 °C. The opposing stream warms from 20 °C to 42.5 °C. Both temperature changes correspond to 113 kW of heat transfer. The streams have different flow rates, so the same heat load produces different changes in temperature.

The Python program runs two independent calculations for each input row. One predicts outlet temperatures for streams flowing in opposite directions. The other predicts how much dissolved material crosses a membrane into a perfect sink. The membrane calculation uses flow, transfer area and a fixed transfer coefficient. Outlet temperature from the heat calculation does not enter it.

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

In the first membrane case, the inlet contains 2.00 mol of solute per cubic meter and the outlet contains 0.736 mol/m³. The balance compares the solute entering each second with the sum leaving in the outlet stream and crossing the membrane.

The second example transfers 207 kW under different inlet conditions, flows and transfer area. Its hot- and cold-side heat balances differ by about 6 × 10⁻¹¹ W. That residual measures arithmetic agreement between the two sides. An exchanger test would be needed to check the outlet predictions against measurements.

The program writes both cases to:

```text
outputs/results.csv
outputs/results.xlsx
```

CSV is the default input. To use Excel, change `INPUT_FILE` in `main.py` to:

```python
INPUT_FILE = "inputs/cases.xlsx"
```

When the two streams have equal heat-capacity rates, the general counter-current formula divides by zero. The code uses its limiting expression for that case. Both models assume positive flow rates, and the membrane calculation assumes positive inlet solute concentration.
