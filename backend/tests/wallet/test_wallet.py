from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.config import STARTING_BALANCE
from backend.wallet.transactions import Transactions

def test_verify_valid_signature():
    data = {'foo':'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key,data,signature)


def test_verify_invalid_sinature():
    data = {'foo':'test_data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data,signature)

def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE
    
    amount = 50
    transaction = Transactions(wallet,'recipient',amount)
    blockchain.add_Block([transaction.to_json()])

    assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE - amount
    
    recieved_amount_1 = 25
    recieved_transaction_1 = Transactions(Wallet(),wallet.address,recieved_amount_1)

    recieved_amount_2 = 35
    recieved_transaction_2 = Transactions(Wallet(),wallet.address,recieved_amount_2)

    blockchain.add_Block([recieved_transaction_1.to_json(),recieved_transaction_2.to_json()])

    assert Wallet.calculate_balance(blockchain,wallet.address) == STARTING_BALANCE - amount + recieved_amount_1 + recieved_amount_2