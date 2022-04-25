import socket
import threading
import argparse
import cryptography


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.block_len = None
        self.public_key = None
        self.secret_key = None
        self.s = None
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs

        # exchange public keys

        # receive the encrypted secret key

        # my code starts
        n, e, secret_key, block_len = self.s.recv(1024).decode().split()
        self.block_len = int(block_len)
        self.public_key = (int(n), int(e))
        self.secret_key = int(secret_key)
        # my code ends

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message, extra = self.s.recv(1024).decode().split()

            # decrypt message with the secrete key

            decrypted_message = cryptography.decrypt_msg(
                message, self.block_len, self.public_key, self.secret_key, int(extra))

            print(decrypted_message)

    def write_handler(self):
        while True:
            message = self.username + ": " + input()

            # encrypt message with the secrete key

            extra, enhanced_msg = cryptography.find_extra_letters(message, self.block_len)
            encrypted_message = cryptography.encrypt_msg(enhanced_msg, self.block_len, self.public_key)

            overall_info = encrypted_message + " " + str(extra)
            self.s.send(overall_info.encode())

            # self.s.send(encrypted_message.encode())
            # print("message sent")
            # self.s.send(str(extra).encode())
            # print("extra sent")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    name = parser.add_argument("name")
    args = parser.parse_args()
    cl = Client("127.0.0.1", 7011, args.name)
    cl.init_connection()
