import os
import sys
import time
from simple_sockets import SimpleSocket
from diffie_hellman import DiffieHellman
from symmetric import Symmetric
from const import BUFFER_SIZE

class Eve:
    def __init__(self, mode):
        self.mode = mode
        self.alice_socket = SimpleSocket('127.0.0.1', 5000)
        self.bob_socket = SimpleSocket('127.0.0.1', 5001)
        self.dh_params = {}

    def relay(self):
        """Relay messages between Alice and Bob without modification."""
        print("[INFO] Starting relay mode.")
        while True:
            data = self.alice_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[RELAY] Alice to Bob: {data}")
            self.bob_socket.send(data)

            data = self.bob_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[RELAY] Bob to Alice: {data}")
            self.alice_socket.send(data)

    def break_heart(self):
        """Change the messages in transit to break the hearts of Alice and Bob."""
        print("[INFO] Starting break-heart mode.")
        while True:
            # Intercept Alice's message and modify it.
            data = self.alice_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[BREAK] Intercepted from Alice: {data}")
            modified_data = b"I hate you!"
            print(f"[BREAK] Modifying message to Bob: {modified_data}")
            self.bob_socket.send(modified_data)

            # Intercept Bob's message and modify it.
            data = self.bob_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[BREAK] Intercepted from Bob: {data}")
            modified_data = b"You broke my heart..."
            print(f"[BREAK] Modifying message to Alice: {modified_data}")
            self.alice_socket.send(modified_data)

    def custom_mode(self):
        """Prompt the user to manually modify the messages being relayed."""
        print("[INFO] Starting custom message mode.")
        while True:
            # Intercept Alice's message.
            data = self.alice_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[CUSTOM] Intercepted from Alice: {data.decode()}")
            custom_message = input("Enter custom message to Bob: ").encode()
            self.bob_socket.send(custom_message)

            # Intercept Bob's message.
            data = self.bob_socket.receive(BUFFER_SIZE)
            if not data:
                break
            print(f"[CUSTOM] Intercepted from Bob: {data.decode()}")
            custom_message = input("Enter custom message to Alice: ").encode()
            self.alice_socket.send(custom_message)

    def start(self):
        self.alice_socket.accept()
        print("[INFO] Connected to Alice.")
        self.bob_socket.accept()
        print("[INFO] Connected to Bob.")

        if self.mode == '--relay':
            self.relay()
        elif self.mode == '--break-heart':
            self.break_heart()
        elif self.mode == '--custom':
            self.custom_mode()
        else:
            print("[ERROR] Unknown mode.")

        self.alice_socket.close()
        self.bob_socket.close()
        print("[INFO] Closed connections.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: eve.py [--relay | --break-heart | --custom]")
        sys.exit(1)

    mode = sys.argv[1]
    eve = Eve(mode)
    eve.start()
