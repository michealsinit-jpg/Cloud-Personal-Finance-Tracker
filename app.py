from flask import Flask, render_template, request, redirect, url_for
from finance_sql import FinanceTracker

app = Flask(__name__)


tracker = FinanceTracker()



@app.route("/")

def home():
    balance = tracker.get_balance()

    income = tracker.get_total_income()

    expense = tracker.get_total_expense()

    transactions = tracker.get_recent_transactions()

    return render_template(

        "index.html",

        balance=balance,

        income=income,

        expense=expense,

        transactions=transactions

    )


@app.route("/add-income", methods=["GET", "POST"])



def add_income():

    if request.method == "POST":

        amount = float(request.form["amount"])

        category = request.form["category"]

        description = request.form["description"]

        date = request.form["date"]

        tracker.add_income_web(

            amount,

            category,

            description,

            date

        )


        return redirect(url_for("home"))

    return render_template("add_income.html")



@app.route("/add-expense", methods=["GET", "POST"])

def add_expense():

    if request.method == "POST":

       amount = float(request.form["amount"])

       category = request.form["category"]

       description = request.form["description"]

       date = request.form["date"]

       tracker.add_expense_web(

           amount,

           category,

           description,

           date

       )

       return redirect(url_for("home"))

    return render_template("add_expense.html")


@app.route("/transactions")

def transactions():

    transactions = tracker.get_all_transactions()

    return render_template(

        "transactions.html",

        transactions=transactions

    )


@app.route("/delete/<int:transaction_id>", methods=["POST"])

def delete_transaction(transaction_id):

    tracker.delete_transaction(transaction_id)

    return redirect(url_for("transactions"))


@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])

def edit_transaction(transaction_id):

    if request.method == "POST":

        transaction_type = request.form["transaction_type"]

        category = request.form["category"]

        description = request.form["description"]

        amount = float(request.form["amount"])

        transaction_date = request.form["date"]

        tracker.update_transaction(

            transaction_id,

            transaction_type,

            category,

            description,

            amount,

            transaction_date

        )

        return redirect(url_for("transactions"))

    transaction = tracker.get_transaction_by_id(transaction_id)

    return render_template(

        "edit_transaction.html",

        transaction=transaction

    )

   

if __name__ == "__main__":

        app.run(debug=True)