import socket
import threading
import argparse
import time
import cryptography
from secrets import compare_digest


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_keys = {}
        self.block_len = None
        self.public_key = None
        self.secret_key = None
        self.s = None
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        """
        Connects the client to the server
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        # sending username to the server
        self.s.send(self.username.encode())

        # generate private and secret keys for a client
        self.public_key, self.secret_key = cryptography.create_keys()
        # gets the length of one block for encrypting
        self.block_len = cryptography.get_block_length(self.public_key[0])
        # sends this info to the server (except secret key)
        self.s.send(f"{self.public_key[0]} {str(self.public_key[1])} {str(self.block_len)}".encode())
        # deadlock problem, the easiest way to solve - wait for another process to finish
        time.sleep(0.01)
        # receiving server keys
        n, e, block_len = self.s.recv(1024).decode().split()
        # saving these keys as an attribute
        self.server_keys = (int(n), int(e), int(block_len))

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        """
        Receives the encoded message from a server
        Checks for message integrity
        """
        while True:
            # receive a message
            received = self.s.recv(1024).decode()
            # get the hash out of the message
            hash_msg = received.split(",")[0]
            # getting the message and the amount of extra letters in it
            message, extra = received.split(",")[1].split()

            # decrypting a massage
            decrypted_message = cryptography.decrypt_msg(
                message, self.block_len, self.public_key, self.secret_key, int(extra))
            # checking if hashes of original message and decrypted one are different
            if compare_digest(str(cryptography.hash_message(decrypted_message)), str(hash_msg)) is False:
                print("Message was received with error")
            else:
                print(decrypted_message)

    def write_handler(self):
        """
        Responsible for sending encrypted messages to the server
        """
        while True:
            message = self.username + ": " + input()
            # separating a message to message and receivers
            message = message.split("|")
            # no receivers mentioned - everyone will receive a message
            if message.__len__() == 1:
                message, receivers = message[0], "ALL"
            else:
                # users separated by space, message keeps the same
                message, receivers = message[0], message[1].split()
            # calculating the hash of the message
            hash_msg = str(cryptography.hash_message(message))
            # getting number of extra letters and a new message
            extra, enhanced_msg = cryptography.find_extra_letters(message, self.server_keys[2])
            # encoding a message
            encrypted_message = cryptography.encrypt_msg(enhanced_msg, self.server_keys[2],
                                                         (self.server_keys[0], self.server_keys[1]))
            # if receivers is an empty list
            if not receivers:
                receivers = "ALL"
            if receivers == "ALL":
                overall_info = f"{hash_msg},{encrypted_message} {extra} ALL"
                # sending message to the server
                self.s.send(overall_info.encode())
                continue
            for username in receivers:
                # no need to send a message to oneself
                if username != self.username:
                    overall_info = f"{hash_msg},{encrypted_message} {extra} {username}"
                    time.sleep(0.01)
                    # sending message to the server
                    self.s.send(overall_info.encode())


if __name__ == "__main__":
    # asking user a nickname
    parser = argparse.ArgumentParser()
    name = parser.add_argument("name")
    args = parser.parse_args()
    cl = Client("127.0.0.1", 7011, args.name)
    cl.init_connection()
