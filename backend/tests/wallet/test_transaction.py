from backend.wallet.transactions import Transactions
from backend.wallet.wallet import Wallet
import pytest # type: ignore
from backend.config import MINE_REWARD,MINING_REWARD_INPUT

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transactions(sender_wallet,recipient,amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transactions(Wallet(),'recipient',9001)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transactions(sender_wallet,'recipient',50)

    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet,'new_recipient',9001)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first recipient'
    first_amount = 50

    transaction = Transactions(sender_wallet, first_recipient, first_amount)

    next_recipient = 'next recipient'
    next_amount = 75
    transaction.update(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - first_amount - next_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

    to_first_amount = 25
    transaction.update(sender_wallet,first_recipient,to_first_amount)

    assert transaction.output[first_recipient]== first_amount + to_first_amount
    assert transaction.output[sender_wallet.address]== sender_wallet.balance - first_amount - next_amount - to_first_amount
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_valid_transaction():
    Transactions.is_valid_transaction(Transactions(Wallet(),'recipient',50))

def test_invalid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transactions(sender_wallet,'recipient',50)
    transaction.output[sender_wallet.address] = 9001

    with pytest.raises(Exception,match = 'Invalid transaction output values'):
        Transactions.is_valid_transaction(transaction)


def test_valid_transaction_with_invalid_outputs():
    transaction = Transactions(Wallet(),'recipient',50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception,match = 'Invalid signature'):
        Transactions.is_valid_transaction(transaction)

def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transactions.reward_transaction(miner_wallet)

    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINE_REWARD

def test_valid_reward_transaction():
    reward_transaction = Transactions.reward_transaction(Wallet())
    Transactions.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_extra_recipiend():
    reward_transaction = Transactions.reward_transaction(Wallet())
    reward_transaction.output['extra_recipient'] = 60

    with pytest.raises(Exception, match = 'Invalid mining reward'):
        Transactions.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transactions.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet.address] = 9001

    with pytest.raises(Exception, match = 'Invalid mining reward'):
        Transactions.is_valid_transaction(reward_transaction)