import pandas as pd

report = pd.read_csv("reconciliation_report.csv")
answer_key = pd.read_csv("answer_key.csv")

report_set = set(zip(report["trade_id"], report["break_type"]))
answer_set = set(zip(answer_key["trade_id"], answer_key["break_type"]))

caught = report_set & answer_set
missed = answer_set - report_set
false_positives = report_set - answer_set

print("Total actual discrepancies:", len(answer_set))
print("Total flagged by tool:", len(report_set))
print("Correctly caught:", len(caught))
print("Missed:", len(missed))
print("False positives:", len(false_positives))