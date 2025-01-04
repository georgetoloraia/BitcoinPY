import argparse
from bitcoin.core.blockchain import Blockchain
from bitcoin.wallet.wallet import Wallet
from bitcoin.core.mining import Miner
from bitcoin.network.p2p import P2PNode

def main():
    parser = argparse.ArgumentParser(description="Bitcoin Node")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address to run the node")
    parser.add_argument("--port", type=int, default=8333, help="Port to run the node")
    parser.add_argument("--mine", action="store_true", help="Enable mining mode")
    parser.add_argument("--wallet", type=str, default=None, help="Path to the wallet file")

    args = parser.parse_args()

    # Initialize Blockchain
    blockchain = Blockchain()

    # Initialize Wallet
    if args.wallet:
        wallet = Wallet.load_wallet(args.wallet)
    else:
        wallet = Wallet()
        wallet.save_wallet("wallet.dat")
        print("New wallet created and saved to 'wallet.dat'.")
    
    # Ensure the wallet has at least one address
    if not wallet.get_address_list():
        new_address = wallet.create_new_key()
        print(f"New mining address created: {new_address}")
    else:
        print(f"Using existing wallet addresses: {wallet.get_address_list()}")
    
    print(f"Starting Bitcoin Node at {args.host}:{args.port}...")


    # Start P2P Node
    p2p_node = P2PNode(host=args.host, port=args.port, blockchain=blockchain)

    if args.mine:
        print("Mining enabled. Starting miner...")
        transaction_pool = []  # Initialize an empty transaction pool
        mining_address = wallet.get_address_list()[0]  # Use the first address in the wallet
        miner = Miner(blockchain=blockchain, transaction_pool=transaction_pool, mining_address=mining_address)
        p2p_node.set_miner(miner)
        miner.start_mining()

    try:
        p2p_node.start_node()
    except KeyboardInterrupt:
        print("Shutting down node...")
        if args.mine:
            miner.stop_mining()
        p2p_node.stop_node()

if __name__ == "__main__":
    main()
