import hashlib
import base58
import os
import requests
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature


def sha256(data):
    """
    Perform a SHA-256 hash on the input data.
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def double_sha256(data):
    """
    Perform a double SHA-256 hash on the input data.
    """
    return sha256(sha256(data))

def generate_address(public_key):
    """
    Generate a Bitcoin-style address from a public key.
    """
    # Ensure the public key is a bytes object
    sha256_hash = hashlib.sha256(public_key).digest()  # No .encode(), public_key is already bytes
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    public_key_hash = ripemd160.digest()

    # Add version byte (0x00 for mainnet)
    versioned_key = b'\x00' + public_key_hash

    # Calculate checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_key).digest()).digest()[:4]

    # Append checksum to the versioned key
    full_key = versioned_key + checksum

    # Convert to Base58
    return base58.b58encode(full_key).decode('utf-8')

def generate_private_key():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    # Convert keys to bytes for storage and usage
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key_bytes, public_key_bytes

def get_public_ip():
    """
    Fetch the public IP address of the node using an external service.
    """
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip", "Unknown")
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return "Unknown"
    
def sign_data(private_key, data):
    """
    Signs the given data using the private key.

    Args:
        private_key: The ECDSA private key object.
        data: The data to sign (string).

    Returns:
        The signature as a hex string.
    """
    signature = private_key.sign(
        data.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    r, s = decode_dss_signature(signature)
    return f"{r:x}:{s:x}"

def verify_signature(public_key, data, signature):
    """
    Verifies a signature using the public key.

    Args:
        public_key: The ECDSA public key object.
        data: The data that was signed (string).
        signature: The signature as a hex string.

    Returns:
        True if the signature is valid, False otherwise.
    """
    r, s = map(lambda x: int(x, 16), signature.split(':'))
    signature_bytes = encode_dss_signature(r, s)
    try:
        public_key.verify(
            signature_bytes,
            data.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception as e:
        return False

class BloomFilter:
    """
    A simple implementation of a Bloom filter for quick membership checks.
    """
    def __init__(self, size=1000):
        self.size = size
        self.bit_array = [0] * size

    def _hashes(self, item):
        """
        Generate multiple hash indices for the given item.
        """
        hash1 = int(hashlib.sha256(item.encode('utf-8')).hexdigest(), 16) % self.size
        hash2 = int(hashlib.md5(item.encode('utf-8')).hexdigest(), 16) % self.size
        return hash1, hash2

    def add(self, item):
        """
        Add an item to the Bloom filter.
        """
        hash1, hash2 = self._hashes(item)
        self.bit_array[hash1] = 1
        self.bit_array[hash2] = 1

    def contains(self, item):
        """
        Check if an item is possibly in the Bloom filter.
        """
        hash1, hash2 = self._hashes(item)
        return self.bit_array[hash1] and self.bit_array[hash2]

# Example Usage
if __name__ == "__main__":
    private_key = generate_private_key()
    print(f"Private Key: {private_key}")

    public_key = sha256(private_key)
    address = generate_address(public_key)
    print(f"Generated Address: {address}")

    ip = get_public_ip()
    print(f"Public IP: {ip}")

    bloom_filter = BloomFilter()
    bloom_filter.add("test-item")
    print(f"Contains 'test-item': {bloom_filter.contains('test-item')}")
    print(f"Contains 'another-item': {bloom_filter.contains('another-item')}")
