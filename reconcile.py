import pandas as pd

ledger = pd.read_csv("internal_ledger.csv")
custodian = pd.read_csv("custodian_statement.csv")

print("Ledger has", len(ledger), "rows.")
print("Custodian has", len(custodian), "rows.")


# FINDING MISSING TRADES
ledger_ids = set(ledger["trade_id"])
custodian_ids = set(custodian["trade_id"])

missing_ids = ledger_ids - custodian_ids

missing_trades = ledger[ledger["trade_id"].isin(missing_ids)]

print("\nMissing trades:", len(missing_trades))
print(missing_trades)

# FINDING DUPLICATE TRADES
duplicate_ids = custodian["trade_id"][custodian["trade_id"].duplicated()]

duplicate_trades = custodian[custodian["trade_id"].isin(duplicate_ids)]

print("\nDuplicate trades:", duplicate_trades["trade_id"].nunique())
print(duplicate_trades.sort_values("trade_id"))

# COMPARING VALUES
matched = pd.merge(
    ledger,
    custodian,
    on="trade_id",
    suffixes=("_ledger", "_custodian")
)

price_breaks = matched[matched["price_ledger"] != matched["price_custodian"]]
quantity_breaks = matched[matched["quantity_ledger"] != matched["quantity_custodian"]]
date_breaks = matched[matched["settle_date_ledger"] != matched["settle_date_custodian"]]

print("\nPrice breaks:", len(price_breaks))
print("Quantity breaks:", len(quantity_breaks))
print("Settlement date breaks:", len(date_breaks))


# CONSOLIDATED REPORT
report_rows = []

for _, row in missing_trades.iterrows():
    report_rows.append({
        "trade_id": row["trade_id"],
        "break_type": "missing_trade",
        "ledger_value": "present",
        "custodian_value": "missing"
    })

for _, row in price_breaks.iterrows():
    report_rows.append({
        "trade_id": row["trade_id"],
        "break_type": "price_variance",
        "ledger_value": row["price_ledger"],
        "custodian_value": row["price_custodian"]
    })

for _, row in quantity_breaks.iterrows():
    report_rows.append({
        "trade_id": row["trade_id"],
        "break_type": "quantity_mismatch",
        "ledger_value": row["quantity_ledger"],
        "custodian_value": row["quantity_custodian"]
    })

for _, row in date_breaks.iterrows():
    report_rows.append({
        "trade_id": row["trade_id"],
        "break_type": "settlement_date_mismatch",
        "ledger_value": row["settle_date_ledger"],
        "custodian_value": row["settle_date_custodian"]
    })

for trade_id in duplicate_ids:
    report_rows.append({
        "trade_id": trade_id,
        "break_type": "duplicate_trade",
        "ledger_value": "single_entry",
        "custodian_value": "duplicated"
    })

report = pd.DataFrame(report_rows)
report.to_csv("reconciliation_report.csv", index=False)

print("\nTotal breaks found:", len(report))