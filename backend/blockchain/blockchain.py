from backend.blockchain.block import Block
from backend.wallet.transactions import Transactions
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet
class Blockchain:
    """
    Blockchain: a public ledger of transactions
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_Block(self, data):
        last_block = self.chain[-1]
        self.chain.append(Block.mine_block(last_block,data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    def replace_chain(self,chain):
        """
        replace the local chain with the incoming one if the following applies:
        - the incoming chain is longer than the local one.
        - the incoming chain is formatted properly.
        """

        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. Incoming chain must be longer')
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. incoming chain is invalid - {e}')

        self.chain = chain
    
    def to_json(self):
        """
        serialize the blockchain into a list of blocks
        """
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize a list of blocks into blockchain instance
        The result will containm a chain list of blockchain instances
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json),chain_json))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        validate incoming chain
        enforce the following rules
        - the chain must start with genesis block
        - blocks must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1,len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block,block)
        
        Blockchain.is_valid_transaction_chain(chain)



    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        this will enforce the rules of the chain composed of blocks of transactions
        - each transaction must only appear once in chain
        - there can only be one mining reward per block
        - each transaction must be valid
        """

        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transactions.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction: {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f'There can only be one mining reward per block.Check block with hash: {block.hash}')
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(historic_blockchain,transaction.input['address'])

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'transaction: {transaction.id} has an invalid input amount')

                Transactions.is_valid_transaction(transaction)






def main():
    blockchain = Blockchain()
    blockchain.add_Block('one')
    blockchain.add_Block('two')

    print(blockchain)

if __name__ == '__main__':
    main()