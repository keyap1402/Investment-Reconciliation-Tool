# Investment Reconciliation Tool

A Python tool that simulates a common investment operations workflow: comparing an internal trade ledger against a custodian statement to identify discrepancies.

## Why I Built This

Investment operations roles rely heavily on accurate, repeatable reconciliation between internal records and external statements. This project simulates that workflow end-to-end — from generating realistic trade data, to injecting known discrepancies, to building a tool that detects them automatically.

## How It Works

1. **`generate_data.py`** — Generates 200 synthetic trades representing an internal ledger (trade ID, dates, security, quantity, price, account).
2. **`generate_discrepancies.py`** — Creates a "custodian statement" version of the same trades, deliberately injecting 5 types of discrepancies at controlled rates: price variance, missing trades, duplicate trades, quantity mismatches, and settlement date mismatches. Every injected discrepancy is logged to `answer_key.csv` for validation.
3. **`reconcile.py`** — Compares the two files and flags all discrepancies, producing `reconciliation_report.csv`.
4. **`validate.py`** — Checks the tool's output against the answer key to confirm detection accuracy.
5. **`build_excel_report.py`** — Generates a formatted Excel workbook (`reconciliation_report.xlsx`) with a summary tab and a detailed breakdown tab.

## Results

The tool correctly identified **29 out of 29** injected discrepancies, with **zero false positives**, validated against a known-answer test set.

## Tech Used

Python, pandas, openpyxl

## How to Run It

1. Clone or download this repository.
2. Install dependencies: `pip install pandas openpyxl`
3. Run the scripts in order:
python generate_data.py
python generate_discrepancies.py
python reconcile.py
python validate.py
python build_excel_report.py


## Files

- `internal_ledger.csv` — synthetic "ground truth" trade data
- `custodian_statement.csv` — same trades with injected discrepancies
- `answer_key.csv` — record of every discrepancy injected (for validation)
- `reconciliation_report.csv` / `reconciliation_report.xlsx` — the tool's output
