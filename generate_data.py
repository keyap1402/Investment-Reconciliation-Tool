import pandas as pd
import random
from datetime import date, timedelta

security_ids = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "JPM", "V"]
account_ids = ["ACC1001", "ACC1002", "ACC1003", "ACC1004", "ACC1005"]
sides = ["BUY", "SELL"]

num_trades = 200
start_date = date(2026, 1, 1)

trades = []

for i in range(num_trades):
    trade_date = start_date + timedelta(days=random.randint(0, 90))
    settle_date = trade_date + timedelta(days=1)

    trade = {
        "trade_id": i + 1,
        "trade_date": trade_date,
        "settle_date": settle_date,
        "security_id": random.choice(security_ids),
        "quantity": random.randint(10, 500),
        "price": round(random.uniform(50, 500), 2),
        "side": random.choice(sides),
        "account_id": random.choice(account_ids),
    }

    trades.append(trade)

df = pd.DataFrame(trades)
df.to_csv("internal_ledger.csv", index=False)

print("Done! Generated", len(df), "trades.")