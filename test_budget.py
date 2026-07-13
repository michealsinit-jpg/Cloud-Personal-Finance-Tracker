from finance_sql import FinanceTracker

tracker = FinanceTracker()

tracker.set_budget(1, 1500)

budget = tracker.get_budget(1)

print("Budget:", budget)