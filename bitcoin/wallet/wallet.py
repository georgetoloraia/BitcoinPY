import os
import pickle
from bitcoin.utils.utils import generate_private_key, generate_address, sign_data, verify_signature

class Wallet:
    def __init__(self, wallet_file="wallet.dat"):
        self.wallet_file = wallet_file
        self.keys = self.load_wallet()

    def save_wallet(self, filename=None):
        """Save the wallet to a specified file."""
        if filename is None:
            filename = self.wallet_file
        with open(filename, "wb") as f:
            pickle.dump(self.keys, f)

    def load_wallet(self):
        """Load the wallet from a file."""
        if os.path.exists(self.wallet_file):
            with open(self.wallet_file, "rb") as f:
                return pickle.load(f)
        return {}

    def create_new_key(self):
        """Generate a new keypair and save it to the wallet."""
        private_key, public_key = generate_private_key()
        address = generate_address(public_key)
        self.keys[address] = {
            'private_key': private_key,
            'public_key': public_key
        }
        self.save_wallet()
        return address

    def get_address_list(self):
        """Return a list of all addresses in the wallet."""
        return list(self.keys.keys())

    def sign_transaction(self, address, data):
        """Sign data using the private key associated with the address."""
        if address not in self.keys:
            raise ValueError("Address not found in wallet.")
        private_key = self.keys[address]['private_key']
        return sign_data(private_key, data)

    def verify_transaction(self, public_key, data, signature):
        """Verify the signature of a transaction."""
        return verify_signature(public_key, data, signature)


# Example usage
if __name__ == "__main__":
    wallet = Wallet()

    # Create a new address
    new_address = wallet.create_new_key()
    print(f"New address created: {new_address}")

    # List all addresses in the wallet
    addresses = wallet.get_address_list()
    print(f"Addresses in wallet: {addresses}")

    # Sign a sample transaction
    sample_data = "Sample transaction data"
    signature = wallet.sign_transaction(new_address, sample_data)
    print(f"Signature: {signature}")

    # Verify the transaction
    public_key = wallet.keys[new_address]['public_key']
    is_valid = wallet.verify_transaction(public_key, sample_data, signature)
    print(f"Signature valid: {is_valid}")
