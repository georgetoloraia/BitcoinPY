import hashlib
import uuid
from typing import List

class CTransaction:
    def __init__(self, sender: str, receiver: str, amount: float, fee: float, timestamp: int):
        self.txid = self.generate_txid()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.timestamp = timestamp
        self.signature = None  # Placeholder for a cryptographic signature

    def generate_txid(self):
        """Generate a unique transaction ID based on transaction data."""
        tx_string = f"{uuid.uuid4()}"
        return hashlib.sha256(tx_string.encode('utf-8')).hexdigest()

    def sign_transaction(self, private_key):
        """Sign the transaction using the sender's private key."""
        if not private_key:
            raise ValueError("Private key is required to sign the transaction")
        # Placeholder for signing logic
        self.signature = f"signed({self.txid})"

    def is_valid(self):
        """Check if the transaction is valid."""
        if self.amount <= 0:
            return False
        if not self.signature:
            return False
        # Add more checks like signature verification if implemented
        return True

    def __repr__(self):
        return (
            f"Transaction(txid={self.txid}, sender={self.sender}, receiver={self.receiver}, "
            f"amount={self.amount}, fee={self.fee}, timestamp={self.timestamp})"
        )

class TransactionPool:
    def __init__(self):
        self.transactions: List[CTransaction] = []

    def add_transaction(self, transaction: CTransaction):
        """Add a transaction to the pool after validation."""
        if transaction.is_valid():
            self.transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction")

    def remove_transaction(self, txid: str):
        """Remove a transaction from the pool by its transaction ID."""
        self.transactions = [tx for tx in self.transactions if tx.txid != txid]

    def get_transactions(self):
        """Return all transactions in the pool."""
        return self.transactions

# Example Usage
if __name__ == "__main__":
    transaction_pool = TransactionPool()

    # Create a transaction
    tx1 = CTransaction(
        sender="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        receiver="1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
        amount=0.5,
        fee=0.0001,
        timestamp=1234567890
    )

    # Sign the transaction (placeholder logic)
    tx1.sign_transaction(private_key="example_private_key")

    # Add the transaction to the pool
    transaction_pool.add_transaction(tx1)

    # Display transactions in the pool
    for tx in transaction_pool.get_transactions():
        print(tx)
