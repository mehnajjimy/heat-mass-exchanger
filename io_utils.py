from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter


def read_cases(path):
    """Read cases from a CSV or Excel file."""

    # Choose the correct pandas reader from the filename ending.
    if path.endswith(".csv"):
        return pd.read_csv(path)
    if path.endswith(".xlsx"):
        return pd.read_excel(path)

    # Stop with a clear message if an unsupported file is supplied.
    raise ValueError("input file must be .csv or .xlsx")


def format_sheet(worksheet, data):
    """Make the Excel output easy to read."""

    # Keep the header visible while scrolling.
    worksheet.freeze_panes = "A2"

    # Set readable widths, but prevent extremely narrow or wide columns.
    for number, column in enumerate(data.columns, start=1):
        worksheet.column_dimensions[get_column_letter(number)].width = min(
            max(len(column) + 2, 14), 30
        )


def save_results(data):
    """Save the same results as CSV and Excel."""

    # Create the output folder if this is the first run.
    Path("outputs").mkdir(exist_ok=True)

    # Save a plain CSV file without an extra pandas row-number column.
    data.to_csv("outputs/results.csv", index=False)

    # Save the same table in Excel and format its results sheet.
    with pd.ExcelWriter("outputs/results.xlsx", engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="results", index=False)
        format_sheet(writer.sheets["results"], data)
