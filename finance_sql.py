from werkzeug.security import generate_password_hash, check_password_hash

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

      VALUES (%s, %s, %s, %s, %s,)

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
   
   def get_total_income(self, user_id):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT SUM(amount)

       FROM transactions

       WHERE user_id = %s
       AND   transaction_type = 'income';

       """

       cursor.execute(sql,(user_id,))

       total = cursor.fetchone()[0] or 0

       self.close_connection(connection, cursor)

       return total

   def get_total_expense(self, user_id):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT SUM(amount)

       FROM transactions

       WHERE user_id = %s
       AND   transaction_type = 'expense';

       """

       cursor.execute(sql, (user_id,))

       total = cursor.fetchone()[0] or 0

       self.close_connection(connection, cursor)

       return total

   def get_balance(self, user_id):

       income = self.get_total_income(user_id)

       expense = self.get_total_expense(user_id)

       return income - expense

   def get_recent_transactions(self, user_id):

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

       WHERE user_id = %s

       ORDER BY transaction_date DESC

       LIMIT 5;

       """

       cursor.execute(sql, (user_id,))

       rows = cursor.fetchall()

       transactions = []

       for row in rows:

           transactions.append(Transaction(*row))

       self.close_connection(connection, cursor)

       return transactions
   

   def add_income_web(self, user_id, amount, category, description, date):

    connection, cursor = self.get_cursor()

    sql = """

    INSERT INTO transactions

    (user_id, transaction_type, category, amount, transaction_date, description)

    VALUES (%s, %s, %s, %s, %s, %s)

    """

    values = (
        user_id,

        "income",

        category,

        amount,

        date,

        description

    )

    cursor.execute(sql, values)

    connection.commit()

    self.close_connection(connection, cursor)




     
   def add_expense_web(self, user_id, amount, category, description, date):

    connection, cursor = self.get_cursor()

    sql = """

    INSERT INTO transactions

    (user_id, transaction_type, category, amount, transaction_date, description)

    VALUES (%s, %s, %s, %s, %s, %s)

    """

    values = (
        user_id,

        "expense",

        category,

        amount,

        date,

        description

    )

    cursor.execute(sql, values)

    connection.commit()

    self.close_connection(connection, cursor)


   def get_all_transactions(self, user_id):

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
       
       WHERE user_id = %s
       
       ORDER BY transaction_date DESC

       """

       cursor.execute(sql, (user_id,))

       rows = cursor.fetchall()

       transactions = []

       for row in rows:

           transactions.append(Transaction(*row))

       self.close_connection(connection, cursor)

       return transactions
   



   def delete_transaction(self, user_id, transaction_id):

       connection = get_connection()

       cursor = connection.cursor()

       query = """

       DELETE FROM transactions

       WHERE user_id = %s
       AND   id = %s

       """

       cursor.execute(query, (user_id, transaction_id,))



       connection.commit()

       cursor.close()

       connection.close() 


   def get_transaction_by_id(self, user_id, transaction_id):

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

      WHERE user_id = %s
      AND id = %s

      """

      cursor.execute(sql, (user_id, transaction_id))

      row = cursor.fetchone()

      if row:


        transaction = Transaction(*row)

      else:
        transaction = None

      self.close_connection(connection, cursor)

      return transaction
   

   def update_transaction(

    self,


    transaction_type,

    category,

    description,

    amount,

    transaction_date,

    user_id,

    transaction_id):

    connection, cursor = self.get_cursor()

    sql = """

    UPDATE transactions

    SET

        transaction_type = %s,

        category = %s,

        description = %s,

        amount = %s,

        transaction_date = %s

    WHERE user_id = %s
    AND   id = %s

    """

    try:
        cursor.execute(sql, (

        transaction_type,

        category,

        description,

        amount,

        transaction_date,

        user_id,

        transaction_id

    

    ))

        if cursor.rowcount == 0:

           print("No transaction was updated.")

        else:

            connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Database error: {e}")

    finally: 
  
       self.close_connection(connection, cursor)


   def register_user(self, username, email, password):

    connection, cursor = self.get_cursor()

    try:

        hashed_password = generate_password_hash(password)

        sql = """

        INSERT INTO users (username, email, password)

        VALUES (%s, %s, %s)

        """

        cursor.execute(sql, (username, email, hashed_password))

        connection.commit()

        return True

    except Exception as e:

        print("Registration Error:", e)

        return False

    finally:

        cursor.close()

        connection.close()



   def get_user_by_email(self, email):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT * FROM users

       WHERE email = %s

       """

       cursor.execute(sql, (email,))

       user = cursor.fetchone()

       cursor.close()

       connection.close()

       return user
   
   def get_spending_by_category(self, user_id):

       connection = get_connection()

       cursor = connection.cursor(dictionary=True)

       query = """

         SELECT category, SUM(amount) AS total

         FROM transactions

         WHERE transaction_type = 'Expense'

         AND user_id = %s

         GROUP BY category

         ORDER BY total DESC

        """

       cursor.execute(query, (user_id,))

       results = cursor.fetchall()

       cursor.close()

       connection.close()

       return results
   

   def get_monthly_spending(self, user_id):

       connection = get_connection()

       cursor = connection.cursor(dictionary=True)

       query = """

         SELECT

         DATE_FORMAT(transaction_date, '%M %Y') AS month,

         SUM(amount) AS total

         FROM transactions

         WHERE transaction_type = 'Expense'

         AND user_id = %s

         GROUP BY

         YEAR(transaction_date),

         MONTH(transaction_date),

         DATE_FORMAT(transaction_date, '%M %Y')

         ORDER BY

         YEAR(transaction_date),

         MONTH(transaction_date)

         """

       cursor.execute(query, (user_id,))

       results = cursor.fetchall()

       cursor.close()

       connection.close()

       return results
   

   def search_transactions(self, user_id, search_term):

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

         WHERE user_id = %s

         AND (

         description LIKE %s

         OR category LIKE %s

         OR transaction_type LIKE %s

         )

       ORDER BY transaction_date DESC

       """

       value = "%" + search_term + "%"

       cursor.execute(sql, (user_id, value, value, value))

       results = cursor.fetchall()

       transactions = []

       for row in results:

         transactions.append(Transaction(*row))

       connection.close()

       return transactions
   

   def set_budget(self, user_id, amount):

      connection, cursor = self.get_cursor()

     # Check if the user already has a budget

      sql = "SELECT * FROM budgets WHERE user_id = %s"

      cursor.execute(sql, (user_id,))

      budget = cursor.fetchone()

      if budget:

        sql = """

        UPDATE budgets

        SET monthly_budget = %s

        WHERE user_id = %s

        """

        cursor.execute(sql, (amount, user_id))

      else:

          sql = """

          INSERT INTO budgets (user_id, monthly_budget)

          VALUES (%s, %s)

          """

          cursor.execute(sql, (user_id, amount))

      connection.commit()

      self.close_connection(connection, cursor)


   def get_budget(self, user_id):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT monthly_budget

       FROM budgets

       WHERE user_id = %s

       """

       cursor.execute(sql, (user_id,))

       result = cursor.fetchone()

       connection.close()

       if result:

          return float(result[0])

       return 0
   

   def get_current_month_expense(self, user_id):

       connection, cursor = self.get_cursor()

       sql = """

       SELECT COALESCE(SUM(amount), 0)

       FROM transactions

       WHERE user_id = %s

       AND transaction_type = 'expense'

       AND MONTH(transaction_date) = MONTH(CURDATE())

       AND YEAR(transaction_date) = YEAR(CURDATE())

       """

       cursor.execute(sql, (user_id,))

       total = cursor.fetchone()[0]

       self.close_connection(connection, cursor)

       return total
   

   def get_remaining_budget(self, user_id):

       budget = self.get_budget(user_id)

       spent = self.get_current_month_expense(user_id)

       return float(budget) - float(spent)