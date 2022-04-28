import socket
import threading
import cryptography
import json


class Server:

    def __init__(self, port: int) -> None:
        self.block_len = None
        self.public_key = None
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.user_keys = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)

            # receiving user's info
            n, e, block_len = c.recv(1024).decode().split()
            # assign user's info to the dictionary
            self.user_keys[username] = (int(n), int(e), int(block_len))
            for client in self.clients:  # after new client has joined, send new dictionary with public keys to everyone
                # get user's info
                user_keys = self.user_keys[self.username_lookup[client]]
                # get new message and number of extra letters
                extra, enhanced_msg = cryptography.find_extra_letters(json.dumps(self.user_keys), user_keys[2])
                # encrypt the message
                message = cryptography.encrypt_msg(message=enhanced_msg, block_len=user_keys[2],
                                                   pub_key=(user_keys[0], user_keys[1]))
                overall_info = message + " dict " + str(extra)
                # send the dictionary to the client
                client.send(overall_info.encode())

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # get user's info
            user_keys = self.user_keys[self.username_lookup[client]]
            # get new message and number of extra letters
            extra, enhanced_msg = cryptography.find_extra_letters(msg, user_keys[2])
            # encrypt the message
            message = cryptography.encrypt_msg(message=enhanced_msg, block_len=user_keys[2],
                                               pub_key=(user_keys[0], user_keys[1]))
            overall_info = message + " " + str(extra)

            client.send(overall_info.encode())

    def handle_client(self, c: socket, addr):
        while True:
            # split a string by spaces to get a message, number of extra letters and sender
            msg, extra, username = c.recv(1024).decode().split()
            for client in self.clients:
                if self.username_lookup[client] == username:  # check whether the receiver is correct
                    client.send(str(msg + " " + extra).encode())


if __name__ == "__main__":
    s = Server(7011)
    s.start()
