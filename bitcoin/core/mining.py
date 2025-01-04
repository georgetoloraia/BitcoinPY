import threading
import time
from hashlib import sha256
from bitcoin.core.blockchain import Blockchain, CBlock

class Miner:
    def __init__(self, blockchain, transaction_pool, mining_address):
        """
        Initializes the miner.
        :param blockchain: The blockchain instance.
        :param transaction_pool: The transaction pool for pending transactions.
        :param mining_address: The address to receive mining rewards.
        """
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool
        self.mining_address = mining_address
        self.is_mining = False

    def start_mining(self):
        self.is_mining = True
        threading.Thread(target=self.mine, daemon=True).start()

    def stop_mining(self):
        self.is_mining = False

    def mine(self):
        print("Mining started...")
        while self.is_mining:
            last_block = self.blockchain.get_last_block()

            # Gather transactions from the transaction pool
            transactions = self.transaction_pool[:]
            reward_transaction = f"Reward Transaction to {self.mining_address}"
            transactions.append(reward_transaction)

            # Create a new block
            new_block = CBlock(
                index=last_block.index + 1,
                prev_hash=last_block.hash,
                transactions=transactions,
                timestamp=int(time.time()),
                nonce=0,
                difficulty=4,  # Adjust difficulty as needed
            )

            # Proof-of-work
            while not new_block.is_valid():
                new_block.nonce += 1
                new_block.hash = new_block.calculate_hash()

                if not self.is_mining:
                    print("Mining stopped.")
                    return

            print(f"Block mined: {new_block.hash}")
            self.blockchain.add_block(new_block)

            # Clear the transaction pool for the next block
            self.transaction_pool.clear()
            time.sleep(1)  # Simulate delay for realistic mining
