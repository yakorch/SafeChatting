import socket
import threading
import argparse
import cryptography
import json


class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.users_dict = {}
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

        # sending username to the server
        self.s.send(self.username.encode())

        # generate private and secret keys for a client
        self.public_key, self.secret_key = cryptography.create_keys()
        # gets the length of one block for encrypting
        self.block_len = cryptography.get_block_length(self.public_key[0])
        # sends this info to the server (except secret key)
        self.s.send((str(self.public_key[0]) + " " + str(self.public_key[1]) + " " + str(self.block_len)).encode())

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self):
        while True:
            # receive a message
            received = self.s.recv(1024).decode()
            # check if it's an encoded dictionary
            if received.split()[1] == "dict":
                # getting required info from the message
                dict_coded, extra = received.split()[0], int(received.split()[2])
                # decoding a dictionary
                decrypted_dict = cryptography.decrypt_msg(
                    dict_coded, self.block_len, self.public_key, self.secret_key, extra)
                # assigning a new dictionary
                self.users_dict = json.loads(decrypted_dict)
                continue

            # if not a dictionary was sent
            message, extra = received.split()

            # decoding a massage
            decrypted_message = cryptography.decrypt_msg(
                message, self.block_len, self.public_key, self.secret_key, int(extra))

            print(decrypted_message)

    def write_handler(self):
        while True:
            message = self.username + ": " + input()
            # separating a message to message and receivers
            message = message.split("|")
            users_info = self.users_dict
            # no receivers mentioned - all will receive a message
            if message.__len__() == 1:
                message, receivers = message[0], users_info.keys()
            else:
                # users separated by space, message keeps the same
                message, receivers = message[0], message[1].split()

            for username in receivers:
                # no need to send a message to oneself
                if username != self.username:
                    try:
                        # finding a receiver
                        user_keys = users_info[username]
                    except KeyError as err:
                        # if username doesn't exist
                        print(f"{username} doesn't exist, try another username")
                        break
                    # getting number of extra letters and new message
                    extra, enhanced_msg = cryptography.find_extra_letters(message, user_keys[2])
                    # encoding a message
                    encrypted_message = cryptography.encrypt_msg(enhanced_msg, user_keys[2], (user_keys[0], user_keys[1]))
                    # complement
                    overall_info = encrypted_message + " " + str(extra) + " " + username
                    # sending info to the server
                    self.s.send(overall_info.encode())


if __name__ == "__main__":
    # asking user a nickname
    parser = argparse.ArgumentParser()
    name = parser.add_argument("name")
    args = parser.parse_args()
    cl = Client("127.0.0.1", 7011, args.name)
    cl.init_connection()
