from finance_sql import FinanceTracker


tracker = FinanceTracker()



while True:

    print("\n===== Cloud Personal Finance Tracker =====")

    print("1. Add Income")

    print("2. Add Expense")

    print("3. View Transactions")

    print("4. View Balance")

    print("5. Spending by Category")

    print("6. Monthly Spending Report")

    print("7.Delete Transactions")

    print("8.Edit Transactions")

    print("9. Search Transactions")

    print("10.Sort By Amount")
    
    print("11. Exit")

    choice = input("Choose an option: ")


    if choice == "1":

        tracker.add_income()

    elif choice == "2":

          tracker.add_expense()


    elif choice == "3":

          tracker.view_transactions()

    elif choice == "4":

          tracker.view_balance()



    elif choice == "5":
          tracker.spending_by_category()

    elif choice == "6":

          tracker.monthly_spending_report()

    elif choice == "7":
         
         tracker.delete_transactions()

    elif choice == "8":
         
         tracker.edit_transactions()

    elif choice == "9":
         

         tracker.search_transactions()


    elif choice == "10":
        
         tracker.sort_by_amount()

            
    elif choice =="11":
        

        print("Goodbye!")

        break

        
    else:
     print("Invalid choice. Try again.")

