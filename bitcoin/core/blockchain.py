import os
import pickle
from hashlib import sha256

class CBlock:
    def __init__(self, index, prev_hash, transactions, timestamp, nonce, difficulty):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_header = f"{self.index}{self.prev_hash}{self.transactions}{self.timestamp}{self.nonce}{self.difficulty}"
        return sha256(block_header.encode('utf-8')).hexdigest()

    def is_valid(self):
        # Validate block hash based on difficulty
        return self.hash.startswith('0' * self.difficulty)

class Blockchain:
    def __init__(self, chain_file='blockchain.dat'):
        self.chain_file = chain_file
        self.chain = self.load_chain()

    def create_genesis_block(self):
        genesis_block = CBlock(0, "0" * 64, "Genesis Block", 0, 0, 4)
        self.chain = [genesis_block]
        self.save_chain()

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        if new_block.prev_hash != self.get_last_block().hash:
            raise ValueError("Invalid previous hash")
        if not new_block.is_valid():
            raise ValueError("Invalid block hash")
        self.chain.append(new_block)
        self.save_chain()

    def save_chain(self):
        with open(self.chain_file, 'wb') as f:
            pickle.dump(self.chain, f)

    def load_chain(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'rb') as f:
                return pickle.load(f)
        else:
            self.create_genesis_block()
            return self.chain

    def display_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.prev_hash}")
            print(f"Hash: {block.hash}")
            print(f"Transactions: {block.transactions}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Nonce: {block.nonce}")
            print(f"Difficulty: {block.difficulty}")
            print("-" * 50)

# Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    # Adding a new block
    last_block = blockchain.get_last_block()
    new_block = CBlock(
        index=last_block.index + 1,
        prev_hash=last_block.hash,
        transactions="Sample Transaction",
        timestamp=1234567890,
        nonce=0,
        difficulty=4
    )

    blockchain.add_block(new_block)
    blockchain.display_chain()
