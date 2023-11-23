from pyteal import *


def time_bank_contract():
    # Define a key for storing time credits
    time_credits = Bytes("time_credits")

    # Handle different transaction types
    handle_creation = Seq(
        [App.globalPut(time_credits, Int(0)), Return(Int(1))]
    )

    handle_opt_in = Return(Int(1))

    handle_closeout = Return(Int(1))

    handle_updateapp = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    # Define a method to add time credits
    add_time_credits = Seq(
        [
            App.globalPut(
                time_credits,
                App.globalGet(time_credits) + Txn.application_args[0],
            ),
            Return(Int(1)),
        ]
    )

    # Choose what to do based on the type of transaction
    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_opt_in],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [
            Txn.on_completion() == OnComplete.UpdateApplication,
            handle_updateapp,
        ],
        [
            Txn.on_completion() == OnComplete.DeleteApplication,
            handle_deleteapp,
        ],
        [Txn.on_completion() == OnComplete.NoOp, add_time_credits],
    )

    return program


# Compile the PyTeal to TEAL
compiled_teal = compileTeal(
    time_bank_contract(), mode=Mode.Application, version=2
)
print(compiled_teal)
