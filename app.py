
import csv

from io import StringIO

from flask import Response
from flask import Flask, render_template, request, redirect, url_for, flash, session
from finance_sql import FinanceTracker
from werkzeug.security import check_password_hash
from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")


tracker = FinanceTracker()



@app.route("/")

def home():

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    balance = tracker.get_balance(session["user_id"])

    income = tracker.get_total_income(session["user_id"])

    expense = tracker.get_total_expense(session["user_id"])

    budget = tracker.get_budget(session["user_id"])

    remaining_budget = tracker.get_remaining_budget(session["user_id"])

    transactions = tracker.get_recent_transactions(session["user_id"])

    

    return render_template(

        "index.html",

        balance=balance,

        income=income,

        expense=expense,

        budget=budget,

        remaining_budget=remaining_budget,

        transactions=transactions

    )


@app.route("/add-income", methods=["GET", "POST"])





def add_income():

    if "user_id" not in session:

       return redirect(url_for("login"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        category = request.form["category"]

        description = request.form["description"]

        date = request.form["date"]

        tracker.add_income_web(
            session["user_id"],

            amount,

            category,

            description,

            date

        )


        return redirect(url_for("home"))

    return render_template("add_income.html")



@app.route("/add-expense", methods=["GET", "POST"])

def add_expense():

    if "user_id" not in session:

       return redirect(url_for("login"))
    
    if request.method == "POST":
       

       amount = float(request.form["amount"])

       category = request.form["category"]

       description = request.form["description"]

       date = request.form["date"]

       tracker.add_expense_web(
           
           session["user_id"],


           amount,

           category,

           description,

           date

       )

       return redirect(url_for("home"))

    return render_template("add_expense.html")


@app.route("/transactions")

def transactions():

    if "user_id" not in session:

        return redirect(url_for("login"))

    search = request.args.get("search")

    if search:

        transactions = tracker.search_transactions(

            session["user_id"],

            search

        )

    else:

        transactions = tracker.get_all_transactions(

            session["user_id"]

        )

    return render_template(

        "transactions.html",

        transactions=transactions,

        search=search

    )


@app.route("/delete/<int:transaction_id>", methods=["POST"])

def delete_transaction(transaction_id):

    if "user_id" not in session:

       return redirect(url_for("login"))

    tracker.delete_transaction(session["user_id"], transaction_id)

    return redirect(url_for("transactions"))


@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])

def edit_transaction(transaction_id):

    if "user_id" not in session:

       return redirect(url_for("login"))

    if request.method == "POST":

        transaction_type = request.form["transaction_type"]

        category = request.form["category"]

        description = request.form["description"]

        amount = float(request.form["amount"])

        transaction_date = request.form["date"]

        tracker.update_transaction(

            transaction_type,

            category,

            description,

            amount,

            transaction_date,

            session["user_id"],

            transaction_id,

         )

        return redirect(url_for("transactions"))

    transaction = tracker.get_transaction_by_id(session["user_id"], transaction_id)

    return render_template(

        "edit_transaction.html",

        transaction=transaction

    )

@app.route("/register", methods=["GET", "POST"])

def register():

    error = None

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            error = "Passwords do not match."

        else:

            success = tracker.register_user(username, email, password)

            if success:

                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))

            else:

                error = "Registration failed. Email may already exist."

    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])

def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = tracker.get_user_by_email(email)

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]

            session["username"] = user[1]

            return redirect(url_for("home"))

        error = "Invalid email or password."

    return render_template("login.html", error=error)


@app.route("/logout")

def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("login"))
   



@app.route("/spending-by-category")

def spending_by_category():

    if "user_id" not in session:

        return redirect(url_for("login"))

    spending = tracker.get_spending_by_category(session["user_id"])

    return render_template(

        "spending_by_category.html",

        spending=spending

    )


@app.route("/monthly-spending")

def monthly_spending():

    if "user_id" not in session:

        return redirect(url_for("login"))

    spending = tracker.get_monthly_spending(session["user_id"])

    return render_template(

        "monthly_spending.html",

        spending=spending

    )


@app.route("/export-csv")

def export_csv():

    if "user_id" not in session:

        return redirect(url_for("login"))

    transactions = tracker.get_all_transactions(session["user_id"])

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",

        "Date",

        "Type",

        "Category",

        "Description",

        "Amount"

    ])

    for transaction in transactions:

        writer.writerow([

            transaction.transaction_id,

            transaction.transaction_date,

            transaction.transaction_type,

            transaction.category,

            transaction.description,

            transaction.amount

        ])

    output.seek(0)
    
    filename = f"transactions_{datetime.now().strftime('%Y-%m-%d')}.csv"

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":

            f"attachment; filename={filename}"

        }

    )



@app.route("/budget", methods=["GET", "POST"])

def budget():

    if "user_id" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        amount = float(request.form["amount"])

        tracker.set_budget(session["user_id"], amount)

        return redirect(url_for("budget"))

    budget = float(tracker.get_budget(session["user_id"]))

    spent = float(tracker.get_current_month_expense(session["user_id"]))

    remaining = budget - spent

    percentage = 0

    if budget > 0:

        percentage = min((spent / budget) * 100, 100)
    progress_color = "green"

    if percentage >= 100:

        progress_color = "red"

    elif percentage >= 80:

        progress_color = "orange"

    status_message = "✅ Great! You're staying within your monthly budget."

    if percentage >= 100:

        status_message = "🚨 Budget exceeded! You have gone over your monthly limit."

    elif percentage >= 80:

       status_message = "⚠️ Warning: You've used over 80% of your monthly budget."


    return render_template(

        "budget.html",

        budget=budget,

        spent=spent,

        remaining=remaining,

        percentage=percentage,

        progress_color=progress_color,

        status_message=status_message
    )

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port, debug=False)