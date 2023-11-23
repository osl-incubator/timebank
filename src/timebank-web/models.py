from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    transactions = db.relationship(
        "Transaction",
        foreign_keys="Transaction.sender_id",
        backref="sender",
        lazy=True,
    )
    received_transactions = db.relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_id",
        backref="receiver",
        lazy=True,
    )


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    amount = db.Column(db.Float)
    algod_txid = db.Column(db.String)  # Algorand Transaction ID
