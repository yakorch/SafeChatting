from random import choice, randint
import discretehelper

helper = discretehelper.helper


def create_primes():
    """
    Returns a list of primes
    """
    return [7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823,
            7829, 7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919]


def make_list(text, length: int) -> list:
    """
    Should create a list, in which each elem has len 'length', out of string
    """
    res = []
    for i in range(len(text) // length):
        res.append(text[i * length:(i + 1) * length])
    return res


class Offset:
    """
    Class for holding the number of extra letters in last block
    """

    def __init__(self, offset=0):
        self.number = offset

    def __str__(self):
        return f"last block contains {self.number} extra letter(s)"

    def __add__(self, numb):
        self.number += numb
        return self


def is_int(numb: int) -> bool:
    """
    Checks whether the number is an integer
    """
    return int(numb) == numb


def encrypt_msg(message: str, block_len: int, pub_key: tuple) -> str:
    """
    Encrypts the message, returns a string of numbers
    'message' - text to be encrypted
    block_len - length of one block
    pub_key - pair (n, e)
    """
    # moving from letters to ascii equivalents
    digit_block = "".join([str(ord(letter) - 32).rjust(2, "0") for letter in message])

    # creating list out of string, each element - one block
    blocks = [digit_block[i * block_len: (i + 1) * block_len]
              for i in range(len(digit_block) // block_len)]

    # creating encoded blocks
    encoded_blocks = list(
        map(lambda block: str(pow(int(block), pub_key[1], pub_key[0])).
            rjust(len(str(pub_key[0])), "0"), blocks))

    return "".join(encoded_blocks)  # creating a string out of coded blocks


def decrypt_msg(text: str, block_len: int, pub_key: tuple, secret_key: int, offset: int = 0) -> str:
    """
    Decrypts a message using client's keys, takes string of numbers?
    'text' - text to be encrypted
    block_len - length of one block
    pub_key - pair (n, e)
    secret_key - secret client's key
    offset - number extra letters
    """
    # conversion from string to blocks
    encode_blocks = make_list(text, length=len(str(pub_key[0])))

    # decoding each element using secret key
    decode_blocks = list(
        map(lambda block: str(pow(int(block), secret_key, pub_key[0])).rjust(block_len, "0"),
            encode_blocks))

    # creating a string out of list, using transition from ascii to chars
    decoded_string = "".join(decode_blocks)
    res = "".join([chr(int(decoded_string[i * 2: (i + 1) * 2]) + 32)
                   for i in range(len(decoded_string) // 2)])

    return res if offset == 0 else res[:-offset]  # depends on whether there are extra letters


def find_extra_letters(message: str, block_len: int) -> int:
    """
    Finds the number of extra letters in the last block
    Returns tuple:
    first elem - number of extra letters
    second elem - new message with random letters in the end if necessary
    """
    lie_offset = Offset()
    new_message = str(message)
    while not is_int(new_message.__len__() / block_len):
        lie_offset += 1
        new_message += chr(randint(32, 122))
    return lie_offset.number, new_message


def create_keys() -> tuple:
    """
    Creates a tuple, first elem - public key, second elem - secret key
    """
    primes = create_primes()
    first_prime = choice(primes)
    second_prime = choice(list(set(primes).difference({first_prime})))  # choosing two different primes
    n = first_prime * second_prime  # first part of open key

    mult_even = (first_prime - 1) * (second_prime - 1)
    e = 3
    while helper.gcd(e, mult_even) != 1:  # second part of open key
        e += 2

    d = helper.opposite_euclid(e, mult_even)  # secret key generator

    return (n, e), d


def get_block_length(public_first_part: int) -> int:
    """
    'public_first_part' - n value, product of two primes
    Returns the length of one block for encoding
    """
    pivot = "90"
    while int(pivot + "90") < public_first_part:
        pivot += "90"
    return pivot.__len__()  # the length of one block for encoding


def test():
    message = "me: nice to meet you"
    (n, e), d = create_keys()
    compare = get_block_length(n)

    offset, message = find_extra_letters(message, compare)

    print(f"message: {message}; n: {n}; e: {e}, d: {d}, block_len: {compare}; offset: {offset}")
    print()

    coded_msg = encrypt_msg(message, compare, (n, e))
    print(f"coded_message: {coded_msg}")
    print()

    decoded = decrypt_msg(coded_msg, compare, (n, e), d, offset)
    print(f"decoded message: {decoded}")
