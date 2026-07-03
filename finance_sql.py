from database import get_connection

from transaction import Transaction

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

class FinanceTracker:
   
   def get_cursor(self):

    connection = get_connection()

    cursor = connection.cursor()

    return connection, cursor

   def close_connection(self, connection, cursor):

       cursor.close()

       connection.close()

   def add_income(self):

       amount = get_valid_amount()

       description = get_valid_description()

       category = get_valid_category()

       date = get_valid_date()

       connection, cursor = self.get_cursor()

    

       

       sql = """

       INSERT INTO transactions

       (transaction_type, category, amount, transaction_date, description)

       VALUES (%s, %s, %s, %s, %s)

       """

       values = (

           "income",

           category,

           amount,

           date,

           description

        )
       try:
           
          cursor.execute(sql, values)

          connection.commit()
          print("income added successfully!")

       except Exception as e:
          
          connection.rollback()

          print(f"Database error: {e}")
          
       finally:
          self.close_connection(connection, cursor)

    



   def add_expense(self):

      amount = get_valid_amount()

      description = get_valid_description()

      category = get_valid_category()

      date = get_valid_date()

      connection, cursor = self.get_cursor()

      sql = """

      INSERT INTO transactions

      (transaction_type, category, amount, transaction_date, description)

      VALUES (%s, %s, %s, %s, %s)

      """

      values = (

          "expense",

          category,

          amount,

          date,

          description

       )

      try:
           
          cursor.execute(sql, values)

          connection.commit()
          print("expense added successfully!")

      except Exception as e:
          
          connection.rollback()

          print(f"Database error: {e}")
          
      finally:
          self.close_connection(connection, cursor)




   def view_transactions(self):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT  id,
                      
                   transaction_type,

                   amount,

                   description,

                   category,

                   transaction_date

        FROM transactions

       """
       try:
           cursor.execute(sql)
           
           transactions = cursor.fetchall()
           if not transactions:

              print("No transactions found.")
           

              return

           print("\n--- Transactions ---")

           for row in transactions:

               transaction = Transaction(*row)

               print(transaction)

       except Exception as e:
           print(f"Database error: {e}")

       finally:
             self.close_connection(connection, cursor)


   def search_transactions(self):
        keyword = input("Enter search keyword: ").strip()
        connection, cursor = self.get_cursor()
        search = f"%{keyword}%"

        
        sql = """
        SELECT id,

               transaction_type,

               amount,

               description,

               category,

               transaction_date

        FROM transactions

        WHERE description LIKE %s

        OR category LIKE %s;
        """
        try:
            cursor.execute(sql, (search, search)) 

            transactions = cursor.fetchall()

            if not transactions:

               print("No matching transactions found.")

               return

            print("\n--- Search Results ---")

            for row in transactions:

                transaction = Transaction(*row)

                print(transaction)

        except Exception as e:

          print(f"Database error: {e}")
        finally:

            self.close_connection(connection, cursor)
       
      
   def delete_transactions(self):
       self.view_transactions()

       connection, cursor = self.get_cursor()
       transaction_id = int(input("Enter transaction ID to delete: "))
       sql = """
       DELETE FROM transactions
       WHERE id = %s 
       """

       try:
           
           cursor.execute(sql, (transaction_id,))

           connection.commit()
           print("transaction deleted successfully!")

       except Exception as e:
          
          connection.rollback()

          print(f"Database error: {e}")
          
       finally:
          self.close_connection(connection, cursor)


   def edit_transactions(self):
       self.view_transactions()
       connection, cursor = self.get_cursor()
       transaction_id = int(input("Enter transaction ID to edit: "))
       transaction_type = input("Enter transaction type (income/expense): ").strip().lower()

       category = get_valid_category()

       amount = get_valid_amount()

       date = get_valid_date()

       description = get_valid_description()
       
       sql = """
       UPDATE transactions
       SET transaction_type = %s,
           category = %s,
           amount = %s,
           transaction_date = %s,
           description = %s
       WHERE id = %s;
       
       """
       
       
       try:
           
           cursor.execute(
               sql, 
               (    transaction_type,
                    category,
                    amount,
                    date,
                    description,
                    transaction_id
                )
           )

           connection.commit()
           print("transaction edited successfully!")

       except Exception as e:
          
          connection.rollback()

          print(f"Database error: {e}")
          
       finally:
          self.close_connection(connection, cursor)


   def monthly_spending_report(self):
       connection, cursor = self.get_cursor()
       sql = """
       SELECT 
           MONTH(transaction_date),
           YEAR(transaction_date),
           SUM(amount)
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY 
        MONTH(transaction_date), 
        YEAR(transaction_date)
        """
       
       cursor.execute(sql)
       transactions = cursor.fetchall()
       
       print("\n--- Monthly Spending Report---")
       for month, year, total in transactions:
           print(f"{year}-{month:02d}: £{total:.2f}")
       
       self.close_connection(connection, cursor)


   def spending_by_category(self):
       connection, cursor = self.get_cursor()
       sql = """
       SELECT

            category,

            SUM(amount)

       FROM transactions

       WHERE transaction_type = 'expense'

       GROUP BY category

       ORDER BY category;
       
       """
       cursor.execute(sql)
       categories = cursor.fetchall()

       print("\n--- Spending by Category ---")

       for category, total in categories:

           print(f"{category}: £{total:.2f}")
       
       self.close_connection(connection, cursor)


   def view_balance(self):
       connection, cursor = self.get_cursor()

       sql = """
       SELECT SUM(amount)

       FROM transactions

       WHERE transaction_type = 'income';
       """
       cursor.execute(sql)
       income = cursor.fetchone()[0] or 0

       sql = """
       SELECT SUM(amount)

       FROM transactions

       WHERE transaction_type = 'expense';
       """

       cursor.execute(sql)
       expense = cursor.fetchone()[0] or 0
       balance = income-expense
       print(f"\nCurrent Balance: £{balance:.2f}")
       
       self.close_connection(connection, cursor)


   def sort_by_amount(self):

    connection, cursor = self.get_cursor()

    sql = """

    SELECT

        id,

        transaction_type,

        amount,

        description,

        category,

        transaction_date

    FROM transactions

    ORDER BY amount ASC;

    """

    cursor.execute(sql)

    transactions = cursor.fetchall()

    if not transactions:

        print("No transactions found.")

        self.close_connection(connection, cursor)


        return

    print("\n--- Transactions Sorted by Amount ---")

    for row in transactions:

        transaction = Transaction(*row)

        print(transaction)

    self.close_connection(connection, cursor)
   
   def get_total_income(self):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT SUM(amount)

       FROM transactions

       WHERE transaction_type = 'income';

       """

       cursor.execute(sql)

       total = cursor.fetchone()[0] or 0

       self.close_connection(connection, cursor)

       return total

   def get_total_expense(self):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT SUM(amount)

       FROM transactions

       WHERE transaction_type = 'expense';

       """

       cursor.execute(sql)

       total = cursor.fetchone()[0] or 0

       self.close_connection(connection, cursor)

       return total

   def get_balance(self):

       income = self.get_total_income()

       expense = self.get_total_expense()

       return income - expense

   def get_recent_transactions(self):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT

          id,

          transaction_type,

          amount,

          description,

          category,

          transaction_date

       FROM transactions

       ORDER BY transaction_date DESC

       LIMIT 5;

       """

       cursor.execute(sql)

       rows = cursor.fetchall()

       transactions = []

       for row in rows:

           transactions.append(Transaction(*row))

       self.close_connection(connection, cursor)

       return transactions
   

   def add_income_web(self, amount, category, description, date):

    connection, cursor = self.get_cursor()

    sql = """

    INSERT INTO transactions

    (transaction_type, category, amount, transaction_date, description)

    VALUES (%s, %s, %s, %s, %s)

    """

    values = (

        "income",

        category,

        amount,

        date,

        description

    )

    cursor.execute(sql, values)

    connection.commit()

    self.close_connection(connection, cursor)




     
   def add_expense_web(self, amount, category, description, date):

    connection, cursor = self.get_cursor()

    sql = """

    INSERT INTO transactions

    (transaction_type, category, amount, transaction_date, description)

    VALUES (%s, %s, %s, %s, %s)

    """

    values = (

        "expense",

        category,

        amount,

        date,

        description

    )

    cursor.execute(sql, values)

    connection.commit()

    self.close_connection(connection, cursor)


   def get_all_transactions(self):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT

          id,

          transaction_type,

          amount,

          description,

          category,

          transaction_date

       FROM transactions

       ORDER BY transaction_date DESC

       """

       cursor.execute(sql)

       rows = cursor.fetchall()

       transactions = []

       for row in rows:

           transactions.append(Transaction(*row))

       self.close_connection(connection, cursor)

       return transactions
   



   def delete_transaction(self, transaction_id):

       connection = get_connection()

       cursor = connection.cursor()

       query = """

       DELETE FROM transactions

       WHERE transaction_id = %s

       """

       cursor.execute(query, (transaction_id,))



       connection.commit()

       cursor.close()

       connection.close() 


   def get_transaction_by_id(self, transaction_id):

      connection, cursor = self.get_cursor()

      sql = """

      SELECT

          id,

          transaction_type,

          amount,

          description,

          category,

          transaction_date

      FROM transactions

      WHERE id = %s

      """

      cursor.execute(sql, (transaction_id,))

      row = cursor.fetchone()

      if row:


        transaction = Transaction(*row)

      else:
        transaction = None

      self.close_connection(connection, cursor)

      return transaction
   

   def update_transaction(

    self,

    transaction_id,

    transaction_type,

    category,

    description,

    amount,

    transaction_date

):

    connection, cursor = self.get_cursor()

    sql = """

    UPDATE transactions

    SET

        transaction_type = %s,

        category = %s,

        description = %s,

        amount = %s,

        transaction_date = %s

    WHERE id = %s

    """

    cursor.execute(sql, (

        transaction_type,

        category,

        description,

        amount,

        transaction_date,

        transaction_id

    ))

    connection.commit()

    self.close_connection(connection, cursor)