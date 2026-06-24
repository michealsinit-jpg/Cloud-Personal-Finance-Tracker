import json
def get_valid_amount():

     while True:

        try:

            amount = float(input("Enter income amount: "))

            if amount > 0:
                return amount

                print("Amount must be greater than 0.")

                

        except ValueError:

           print("Please enter a valid number.")

def get_valid_description():
     while True:

       description = input("Enter description: ").strip()

       if description:

           return description

       print("Description cannot be empty.")

def get_valid_category():
 
     while True:

       category = input("Enter category: ").strip()

       if category:

           return category

       print("Category cannot be empty.")


from datetime import datetime

def get_valid_date():

    while True:

        date = input(

            "Enter date (YYYY-MM-DD): "

        ).strip()

        try:

            datetime.strptime(

                date,

                "%Y-%m-%d"

            )

            return date

        except ValueError:

            print(

                "Invalid date. "

                "Use YYYY-MM-DD format."

            )


def load_data():

    with open("data.json", "r") as file:

        return json.load(file)

def save_data(data):

    with open("data.json", "w") as file:

        json.dump(data, file, indent=4)

class FinanceTracker:
     
     def __init__(self):
         self.data = load_data()
     
     def add_income(self):


         amount = get_valid_amount()
         description = get_valid_description()
         category = get_valid_category()
         Date =get_valid_date()

    

         transaction = {

             "type": "income",

             "amount": amount,

             "description": description,

             "category": category,
             "Date": Date

         }

         self.data["transactions"].append(transaction)
     
         save_data(self.data)
         print("Income added successfully!")

     def add_expense(self):

         amount = get_valid_amount()
         description = get_valid_description()
         category = get_valid_category()


         Date = get_valid_date()

         transaction = {

           "type": "expense",

           "amount": amount,

            "description": description,
           "category": category,

            "Date": Date

         }

         self.data["transactions"].append(transaction)

         save_data(self.data)

         print("Expense added successfully!")

     def view_transactions(self):

         print("\n--- Transactions ---")

         for index, transaction in enumerate(self.data["transactions"], start=1):

             description = transaction.get(

                "description",

                "No description"

             )

             category = transaction.get(

                "category",

                "No category"

             )

             Date = transaction.get(
              "Date",
              "No Date"
             )

             print(
             f"{index}."
             f"{transaction['type'].title()} -  "

              f"£{transaction['amount']} - "

              f"{description} "
              f"({category})"
              f"[{Date}]"
             )

     def view_balance(self):

         balance = 0

         for transaction in self.data["transactions"]:

            if transaction["type"] == "income":

                balance += transaction["amount"]

            elif transaction["type"] == "expense":

                balance -= transaction["amount"]

         print(f"\nCurrent Balance: £{balance}")


     def spending_by_category(self):

        categories = {}

        for transaction in self.data["transactions"]:

            if transaction["type"] == "expense":

                category = transaction.get(

                   "category",

                   "Uncategorized"

                 )

                categories[category] = (

                categories.get(category, 0)

                + transaction["amount"]

               )

        print("\n--- Spending by Category ---")

        for category, amount in categories.items():

            print(f"{category}: £{amount}")

     def monthly_spending_report(self):

        monthly_totals = {}

        for transaction in self.data["transactions"]:

            if transaction["type"] == "expense":

               Date = transaction.get("Date", "")

               month = Date[:7]

               monthly_totals[month] = (

                monthly_totals.get(month, 0)

                + transaction["amount"]

             )

            print("\n--- Monthly Spending Report ---")

        for month, amount in monthly_totals.items():

         print(f"{month}: £{amount}")


     def delete_transaction(self):

         self.view_transactions()

         choice = int(input("Enter transaction number to delete: "))

         if 1 <= choice <= len(self.data["transactions"]):

             deleted = self.data["transactions"].pop(choice - 1)

             save_data(self.data)

             print(

                 f"Deleted: {deleted['description']}"

             )

         else:

             print("Invalid transaction number.")

     def edit_transaction(self):

        self.view_transactions()

        choice = int(input("Enter transaction number to edit: "))

        if 1 <= choice <= len(self.data["transactions"]):

            transaction = self.data["transactions"][choice - 1]
           
            new_description = input(

               f"New description ({transaction['description']}): "

             )
            
            if new_description:

                transaction["description"] = new_description

            new_amount = input(

                f"New amount ({transaction['amount']}): "

             )

            if new_amount:

                transaction["amount"] = float(new_amount)

            

            new_category = input(

                f"New category ({transaction['category']}): "

             )

            if new_category:

                transaction["category"] = new_category

            

            new_Date = input(

               f"New Date ({transaction['Date']}): "

             )

            if new_Date:

                transaction["Date"] = new_Date

            save_data(self.data)

            print("Transaction updated!")

        else:


             print("Invalid transaction number.")


     def search_transactions(self):

         keyword = input(

             "Enter description or category: "

             ).lower()

         found = False

         for transaction in self.data["transactions"]:

             description = transaction.get(

                 "description",

                 ""

                 ).lower()

             category = transaction.get(

                 "category",

                 ""

                  ).lower()

             if (

                 keyword in description

                 or keyword in category

                 ):

                 print(

                     f"{transaction['type'].title()} - "

                     f"£{transaction['amount']} - "

                     f"{transaction['description']} "

                     f"({transaction['category']})"

                 )

                 found = True

         if not found:

             print("No matching transactions found.")


     def sort_by_amount(self):

         transactions = sorted(

             self.data["transactions"],

             key=lambda t: t["amount"]

         )

         for transaction in transactions:

             print(

                 f"{transaction['type']} - "

                 f"£{transaction['amount']}"

             )


             