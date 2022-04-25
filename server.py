import socket
import threading
import cryptography


class Server:

    def __init__(self, port: int) -> None:
        self.block_len = None
        self.public_key = None
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # my code starts

        (n, e), d = cryptography.create_keys()
        block_len = cryptography.get_block_length(n)
        self.block_len = block_len
        self.public_key = (int(n), int(e))

        # my code ends

        # generate keys ...

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)

            # send public key to the client

            # public key - pair (n, e)

            # ...

            # encrypt the secret with the clients public key

            # ...

            # send the encrypted secret to a client

            # ...

            # my code starts

            # send a pair (n, e, d) - a public key and a private key
            c.send(f"{n} {e} {d} {block_len}".encode())

            # my code ends

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # encrypt the message

            extra, enhanced_msg = cryptography.find_extra_letters(msg, self.block_len)
            message = cryptography.encrypt_msg(message=enhanced_msg, block_len=self.block_len, pub_key=self.public_key)
            overall_info = message + " " + str(extra)

            client.send(overall_info.encode())

    def handle_client(self, c: socket, addr):  # delete address
        while True:
            msg = c.recv(1024)
            for client in self.clients:
                if client != c:
                    client.send(msg)


if __name__ == "__main__":
    s = Server(7011)
    s.start()
