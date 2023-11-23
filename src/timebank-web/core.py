from algosdk.v2client import algod
from algosdk import account

from .models import Member, Transaction, db


# Algorand client setup
algod_address = "http://localhost:4001"  # or your Algorand node address
algod_token = "your-algod-token"
algod_client = algod.AlgodClient(algod_token, algod_address)


def has_sufficient_credits(member_id: int, required_credits: float):
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Assuming member_id is the Algorand address of the member
    account_info = algod_client.account_info(member_id)

    # The balance is in microAlgos
    balance_microalgos = account_info.get("amount")

    # Convert required credits to microAlgos if necessary
    required_microalgos = (
        required_credits * 1_000_000
    )  # Example conversion rate

    return balance_microalgos >= required_microalgos


def submit_transaction_to_algorand(
    sender_id, receiver_id, amount, sender_mnemonic
):
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Retrieve parameters for the transaction
    params = algod_client.suggested_params()

    # Convert the amount to microAlgos
    amount_microalgos = amount * 1_000_000  # Example conversion

    # Generate the sender's account address from the mnemonic
    sender_sk = mnemonic.to_private_key(sender_mnemonic)
    sender_address = account.address_from_private_key(sender_sk)

    # Create a payment transaction
    algod_txn = transaction.PaymentTxn(
        sender_address, params, receiver_id, amount_microalgos
    )

    # Sign the transaction
    signed_txn = algod_txn.sign(sender_sk)

    # Send the transaction
    txid = algod_client.send_transaction(signed_txn)

    return txid


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
