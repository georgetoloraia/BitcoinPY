# BitcoinPY: A Python-Based Blockchain Implementation

BitcoinPY is a Python-based blockchain project featuring wallet management, mining, and a peer-to-peer networking system. This project aims to provide a simple yet extensible blockchain platform for developers and enthusiasts.

---

## Features
- **Blockchain**: A lightweight, pickle-based blockchain for efficient storage and retrieval.
- **Wallet**: Manage Bitcoin addresses, sign transactions, and verify signatures.
- **Mining**: Mine blocks using proof-of-work and receive rewards.
- **P2P Networking**: Peer-to-peer connections for block and transaction propagation.

---

## Requirements
- **Python**: Version 3.7 or higher.
- **Dependencies**:
  - `cryptography`
  - `flask`

Install dependencies via:
```bash
pip install -r requirements.txt
```

## Installation
- **Clone the Repository**:
```bash
git clone https://github.com/georgetoloraia/BitcoinPY.git
cd BitcoinPY
```

- **Setup Virtual Environment (Recommended)**:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

- **Compile and Install**
```bash
python setup.py install
```

## Usage
- **Start a Bitcoin node:**
```bash
python main.py --host <HOST> --port <PORT>
```
- **Example**
```bash
python main.py --host 192.168.0.100 --port 8333
```

## Enable Mining
- **To start mining:**
```bash
python main.py --host <HOST> --port <PORT> --mine
```

- **Example**
```bash
python main.py --host 192.168.0.100 --port 8333 --mine
```

## Wallet Management
1. A new wallet is automatically created on the first run and saved as `wallet.dat`.
2. Existing wallets are loaded automatically for mining or transactions.


## How It Works
### Blockchain
- Blocks are stored in a `.dat` file using Python's `pickle` for serialization.
- The chain starts with a **genesis block**.

### Mining
- **Proof-of-Work**: Miners calculate a valid hash to add new blocks.
- **Reward**: Newly mined blocks reward the miner.

### P2P Networking
- Nodes communicate via a peer-to-peer protocol.
- The bootstrap node is `5.178.148.11:8333`.

## Development
### Project Structure ()
```plaintext
BitcoinPY/
├── bitcoin/
│   ├── core/                 # Blockchain and transaction logic
│   │   ├── blockchain.py
│   │   ├── transaction.py
│   ├── wallet/               # Wallet management
│   │   ├── wallet.py
│   ├── network/              # P2P networking
│   │   ├── p2p.py
│   ├── utils/                # Utility functions
│       ├── utils.py
├── main.py                   # Entry point for running the node
├── requirements.txt          # Python dependencies
├── setup.py                  # Installation and packaging script
└── README.md                 # Project documentation
```

## Contribution
- Contributions are welcome! Submit a pull request or report issues in the **GitHub** repository.


# FAQ
1. **How do I connect two nodes?**
- Start one node as the bootstrap node:
```bash
python main.py --host 192.168.0.100 --port 8333
```
- Start a second node and connect to the bootstrap:
```bash
python main.py --host 192.168.0.101 --port 8334
```

2. **Where are the blockchain and wallet stored?**
- **Blockchain**: Stored in `blockchain.dat`.
- **Wallet**: Stored in `wallet.dat`.

## License
This project is licensed under the MIT License. See `LICENSE` for details.