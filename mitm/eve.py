import os
import sys
import time
from simple_sockets import SimpleSocket
from diffie_hellman import DH
from symmetric import Symmetric
from const import BUFFER_SIZE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Eve:
    def __init__(self, mode):
        self.mode = mode
        self.alice_socket = SimpleSocket('127.0.0.1', 5000)
        self.bob_socket = SimpleSocket('127.0.0.1', 5001)
        # Removed unused DiffieHellman import and related attributes

    def relay(self):
        """Relay messages between Alice and Bob without modification."""
        logger.info("Starting relay mode.")
        while True:
            try:
                data = self.alice_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[RELAY] Alice to Bob: {data}")
                self.bob_socket.send(data)

                data = self.bob_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[RELAY] Bob to Alice: {data}")
                self.alice_socket.send(data)
            except Exception as e:
                logger.error(f"[ERROR] Relay failed: {e}")
                break

    def break_heart(self):
        """Change the messages in transit to break the hearts of Alice and Bob."""
        logger.info("Starting break-heart mode.")
        while True:
            try:
                # Intercept Alice's message and modify it.
                data = self.alice_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[BREAK] Intercepted from Alice: {data}")
                modified_data = b"I hate you!"
                logger.info(f"[BREAK] Modifying message to Bob: {modified_data}")
                self.bob_socket.send(modified_data)

                # Intercept Bob's message and modify it.
                data = self.bob_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[BREAK] Intercepted from Bob: {data}")
                modified_data = b"You broke my heart..."
                logger.info(f"[BREAK] Modifying message to Alice: {modified_data}")
                self.alice_socket.send(modified_data)
            except Exception as e:
                logger.error(f"[ERROR] Break-heart failed: {e}")
                break

    def custom_mode(self):
        """Prompt the user to manually modify the messages being relayed."""
        logger.info("Starting custom message mode.")
        while True:
            try:
                # Intercept Alice's message.
                data = self.alice_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[CUSTOM] Intercepted from Alice: {data.decode()}")
                custom_message = input("Enter custom message to Bob: ").encode()
                if not custom_message:
                    custom_message = data  # Use original message if no input
                self.bob_socket.send(custom_message)

                # Intercept Bob's message.
                data = self.bob_socket.receive(BUFFER_SIZE)
                if not data:
                    break
                logger.info(f"[CUSTOM] Intercepted from Bob: {data.decode()}")
                custom_message = input("Enter custom message to Alice: ").encode()
                if not custom_message:
                    custom_message = data  # Use original message if no input
                self.alice_socket.send(custom_message)
            except Exception as e:
                logger.error(f"[ERROR] Custom mode failed: {e}")
                break

    def start(self):
        try:
            self.alice_socket.accept()
            logger.info("Connected to Alice.")
            self.bob_socket.accept()
            logger.info("Connected to Bob.")

            if self.mode == '--relay':
                self.relay()
            elif self.mode == '--break-heart':
                self.break_heart()
            elif self.mode == '--custom':
                self.custom_mode()
            else:
                logger.error("Unknown mode.")

        except Exception as e:
            logger.error(f"[ERROR] Connection failed: {e}")

        finally:
            self.alice_socket.close()
            self.bob_socket.close()
            logger.info("Closed connections.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: eve.py [--relay | --break-heart | --custom]")
        sys.exit(1)

    mode = sys.argv[1]
    eve = Eve(mode)
    eve.start()
