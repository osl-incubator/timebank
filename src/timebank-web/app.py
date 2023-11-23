from algosdk import mnemonic
from algosdk import transaction
from algosdk.v2client import algod
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import db, Member, Transaction

app = Flask(__name__, template_folder="templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)
migrate = Migrate(app, db)

# Algorand client setup
algod_address = "http://localhost:4001"  # or your Algorand node address
algod_token = "your-algod-token"
algod_client = algod.AlgodClient(algod_token, algod_address)


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
            sender_id, receiver_id, amount
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


def create_transaction(data):
    member_id = data["member_id"]
    amount = data["amount"]

    # Create a transaction to interact with the PyTeal smart contract
    params = algod_client.suggested_params()

    # Smart Contract Application ID
    app_id = 123456  # Replace with your actual app ID

    # Example arguments for the smart contract call
    app_args = [member_id.to_bytes(8, "big"), int(amount).to_bytes(8, "big")]

    # Algorand account setup (replace with actual addresses and mnemonic)
    sender_address = "your-sender-address"
    sender_mnemonic = "your-sender-mnemonic"
    sender_sk = mnemonic.to_private_key(sender_mnemonic)

    algod_txn = transaction.ApplicationCallTxn(
        sender=sender_address,
        sp=params,
        index=app_id,
        on_complete=transaction.OnComplete.NoOpOC,
        app_args=app_args,
    )

    # Sign and send the transaction
    signed_txn = algod_txn.sign(sender_sk)
    txid = algod_client.send_transaction(signed_txn)

    # Save transaction in the database (after successful blockchain interaction)
    flask_transaction = Transaction(member_id=member_id, amount=amount)
    db.session.add(flask_transaction)
    db.session.commit()

    return jsonify(
        {
            "id": flask_transaction.id,
            "member_id": flask_transaction.member_id,
            "amount": flask_transaction.amount,
            "algod_txid": txid,
        }
    )


def get_transactions():
    transactions = Transaction.query.all()
    enhanced_transactions = []

    for t in transactions:
        algod_data = fetch_algorand_transaction_data(
            t.algod_txid
        )  # Implement this function
        transaction_info = {
            "id": t.id,
            "member_id": t.member_id,
            "amount": t.amount,
            "algod_txid": t.algod_txid,
            "algod_data": algod_data,
        }
        enhanced_transactions.append(transaction_info)

    return enhanced_transactions


if __name__ == "__main__":
    app.run(
        debug=True,
        passthrough_errors=True,
        use_debugger=True,
        use_reloader=True,
    )
