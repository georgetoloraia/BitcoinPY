import socket
import threading
import requests
import time
from bitcoin.core.blockchain import Blockchain


class P2PNode:
    def __init__(self, host="0.0.0.0", port=8333, bootstrap_ip="5.178.148.11", bootstrap_port=8333, blockchain=None):
        self.host = host
        self.port = port
        self.bootstrap_ip = bootstrap_ip
        self.bootstrap_port = bootstrap_port
        self.blockchain = blockchain or Blockchain()
        self.peers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.miner = None

    def set_miner(self, miner):
        """
        Associate a miner with this P2PNode.
        """
        self.miner = miner

    def get_public_ip(self):
        """
        Fetch the public IP address using an external service.
        """
        try:
            public_ip = requests.get("https://api64.ipify.org").text
            print(f"Public IP: {public_ip}")
            return public_ip
        except Exception as e:
            print(f"Error fetching public IP: {e}")
            return None

    def start_node(self):
        """
        Start the P2P node and attempt to connect to the bootstrap node.
        """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Node started at {self.host}:{self.port}")

            # Get public IP
            public_ip = self.get_public_ip()
            if public_ip:
                print(f"Publicly accessible at {public_ip}:{self.port}")

            # Try to connect to bootstrap node
            if self.bootstrap_ip and self.bootstrap_port:
                self.connect_to_peer(self.bootstrap_ip, self.bootstrap_port)

            # Start listening for peers
            threading.Thread(target=self.listen_for_peers, daemon=True).start()

            # Start mining if a miner is set
            if self.miner:
                threading.Thread(target=self.miner.start_mining, daemon=True).start()

        except Exception as e:
            print(f"Failed to start node: {e}")

    def listen_for_peers(self):
        """
        Listen for incoming connections from peers.
        """
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"Connected to peer: {address}")
                self.peers.append(client_socket)
                threading.Thread(target=self.handle_peer, args=(client_socket,)).start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    def handle_peer(self, peer_socket):
        """
        Handle communication with a peer.
        """
        try:
            while True:
                data = peer_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received from peer: {message}")
                self.process_message(message)
        except Exception as e:
            print(f"Error handling peer: {e}")
        finally:
            peer_socket.close()
            if peer_socket in self.peers:
                self.peers.remove(peer_socket)

    def process_message(self, message):
        """
        Process a message received from a peer.
        """
        print(f"Processing message: {message}")
        # Add logic for processing blockchain or mining-related messages

    def broadcast(self, message, exclude=None):
        """
        Broadcast a message to all connected peers, except one.
        """
        for peer in self.peers:
            if peer is not exclude:
                try:
                    peer.sendall(message.encode())
                except Exception as e:
                    print(f"Error broadcasting to peer: {e}")
                    if peer in self.peers:
                        self.peers.remove(peer)

    def connect_to_peer(self, ip, port):
        """
        Connect to a peer at a given IP and port.
        """
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((ip, port))
            self.peers.append(peer_socket)
            print(f"Connected to peer at {ip}:{port}")
            threading.Thread(target=self.handle_peer, args=(peer_socket,)).start()
        except Exception as e:
            print(f"Failed to connect to {ip}:{port}: {e}")


if __name__ == "__main__":
    # Example usage
    node = P2PNode(host="0.0.0.0", port=8333, bootstrap_ip="5.178.148.11", bootstrap_port=8333)
    node.start_node()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Node shutting down...")
