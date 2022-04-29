import socket
import threading
import cryptography


class Server:

    def __init__(self, port: int) -> None:
        self.secret_key = None
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

        # creating server keys
        self.public_key, self.secret_key = cryptography.create_keys()
        self.block_len = cryptography.get_block_length(self.public_key[0])

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

            c.send((str(self.public_key[0]) + " " + str(self.public_key[1]) + " " + str(self.block_len)).encode())

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # get user's info
            user_keys = self.user_keys[self.username_lookup[client]]
            client.send(self.create_string(msg, user_keys).encode())

    def handle_client(self, c: socket, addr):
        while True:
            was_sent = False
            # split a string by spaces to get a message, number of extra letters and receiver
            msg, extra, username = c.recv(1024).decode().split()
            # decrypting a message with server keys
            decrypted_message = cryptography.decrypt_msg(
                msg, self.block_len, self.public_key, self.secret_key, int(extra))

            for client in self.clients:
                if username == "ALL":
                    if client != c:
                        # getting keys of a specific user
                        user_keys = self.user_keys[self.username_lookup[client]]
                        # sending the encrypted message
                        client.send(self.create_string(decrypted_message, user_keys).encode())
                        was_sent = True
                else:
                    if self.username_lookup[client] == username:  # check whether the receiver is correct
                        # getting keys of a specific user
                        user_keys = self.user_keys[username]
                        # sending the encrypted message
                        client.send(self.create_string(decrypted_message, user_keys).encode())
                        was_sent = True
            if was_sent is False:
                # if the username is incorrect
                message = f"{username} doesn't exist, try another username"
                user_keys = self.user_keys[self.username_lookup[c]]
                c.send(self.create_string(message, user_keys).encode())

    @staticmethod
    def create_string(message: str, user_keys: tuple) -> str:
        """
        Creates an encoded string with extra letters
        using tuple 'user_keys' - (n, e, block length) for RSA
        """
        # get new message and number of extra letters
        extra, enhanced_msg = cryptography.find_extra_letters(message, user_keys[2])
        # encrypt the message
        encrypted_message = cryptography.encrypt_msg(enhanced_msg, user_keys[2], (user_keys[0], user_keys[1]))
        # message with the number of extra letters
        return str(encrypted_message + " " + str(extra))


if __name__ == "__main__":
    s = Server(7011)
    s.start()
