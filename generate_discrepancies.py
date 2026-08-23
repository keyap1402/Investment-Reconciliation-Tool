import pandas as pd
import random

#LOADING THE LEDGER
random.seed(42)

df = pd.read_csv("internal_ledger.csv")
custodian = df.copy()
answer_key = []

#PRICE VARIANCE
price_variance_count = int(len(custodian) * 0.05)
price_variance_rows = random.sample(range(len(custodian)), price_variance_count)

for idx in price_variance_rows:
    original_price = custodian.loc[idx, "price"]
    new_price = round(original_price * random.uniform(1.001, 1.02), 2)
    custodian.loc[idx, "price"] = new_price

    answer_key.append({
        "trade_id": custodian.loc[idx, "trade_id"],
        "break_type": "price_variance",
        "original_value": original_price,
        "new_value": new_price
    })

# MISSING TRADES
missing_count = int(len(custodian) * 0.03)
missing_rows = random.sample(range(len(custodian)), missing_count)

for idx in missing_rows:
    answer_key.append({
        "trade_id": custodian.loc[idx, "trade_id"],
        "break_type": "missing_trade",
        "original_value": "present",
        "new_value": "removed"
    })

custodian = custodian.drop(index=missing_rows).reset_index(drop=True)

# DUPLICATE TRADES
duplicate_count = int(len(custodian) * 0.02)
duplicate_rows = random.sample(range(len(custodian)), duplicate_count)

for idx in duplicate_rows:
    answer_key.append({
        "trade_id": custodian.loc[idx, "trade_id"],
        "break_type": "duplicate_trade",
        "original_value": "single_entry",
        "new_value": "duplicated"
    })

duplicated_data = custodian.loc[duplicate_rows]
custodian = pd.concat([custodian, duplicated_data], ignore_index=True)

# QUANTITY MISMATCH
quantity_count = int(len(custodian) * 0.03)
quantity_rows = random.sample(range(len(custodian)), quantity_count)

for idx in quantity_rows:
    original_qty = custodian.loc[idx, "quantity"]
    new_qty = original_qty + random.choice([-10, -5, 5, 10, 20])
    custodian.loc[idx, "quantity"] = new_qty

    answer_key.append({
        "trade_id": custodian.loc[idx, "trade_id"],
        "break_type": "quantity_mismatch",
        "original_value": original_qty,
        "new_value": new_qty
    })

# SETTLEMENT DATE MISMATCH
date_count = int(len(custodian) * 0.03)
date_rows = random.sample(range(len(custodian)), date_count)

for idx in date_rows:
    original_date = custodian.loc[idx, "settle_date"]
    custodian.loc[idx, "settle_date"] = str((pd.to_datetime(original_date) + pd.Timedelta(days=1)).date())

    answer_key.append({
        "trade_id": custodian.loc[idx, "trade_id"],
        "break_type": "settlement_date_mismatch",
        "original_value": original_date,
        "new_value": custodian.loc[idx, "settle_date"]
    })



custodian.to_csv("custodian_statement.csv", index=False)

answer_key_df = pd.DataFrame(answer_key)
answer_key_df.to_csv("answer_key.csv", index=False)

print("Done! Custodian file has", len(custodian), "rows.")
print("Answer key has", len(answer_key_df), "logged discrepancies.")