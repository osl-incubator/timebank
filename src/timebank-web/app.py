from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_migrate import Migrate

from .core import has_sufficient_credits, get_transactions
from .models import Member, Transaction, db

app = Flask(__name__, template_folder="templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


# Members


@app.route("/members/")
def members_list():
    members = Member.query.all()
    return render_template("members/list.html", members=members)


@app.route("/members/form", methods=["GET", "POST"])
def member_create():
    template_file = "members/form.html"
    if request.method == "POST":
        try:
            name = request.form["name"]
            new_member = Member(name=name)
            db.session.add(new_member)
            db.session.commit()
            return redirect(url_for("members_list"))
        except:
            return render_template(template_file, error="An error occurred.")
    return render_template(template_file)


@app.route("/members/edit/<int:id>", methods=["GET", "POST"])
def member_edit(id):
    template_file = "members/form.html"
    member = Member.query.get_or_404(id)
    if request.method == "POST":
        try:
            member.name = request.form["name"]
            db.session.commit()
            return redirect(url_for("members_list"))
        except Exception as e:
            return render_template(
                template_file, member=member, error=f"An error occurred: {e}."
            )
    return render_template(template_file, member=member)


# Transactions


@app.route("/transactions/")
def transactions_list():
    transactions = get_transactions()
    return render_template("transactions/list.html", transactions=transactions)


@app.route("/transactions/form", methods=["GET", "POST"])
def transaction_create():
    template_file = "transactions/form.html"
    if request.method == "POST":
        sender_id = request.form["sender_id"]
        receiver_id = request.form["receiver_id"]
        amount = float(request.form["amount"])

        # Check if the sender has enough credits using Algorand SDK
        if not has_sufficient_credits(sender_id, amount):
            return render_template(
                template_file, error="Insufficient credits."
            )

        # Create and submit the transaction to Algorand blockchain
        algod_txid = submit_transaction_to_algorand(
            sender_id, receiver_id, amount, {}
        )

        # Save the transaction in the database
        new_transaction = Transaction(
            sender_id=sender_id,
            receiver_id=receiver_id,
            amount=amount,
            algod_txid=algod_txid,
        )
        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for("transactions_list"))

    return render_template(template_file)


if __name__ == "__main__":
    app.run(
        debug=True,
        passthrough_errors=True,
        use_debugger=True,
        use_reloader=True,
    )
