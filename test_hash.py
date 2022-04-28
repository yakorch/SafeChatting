from hashlib import sha256
from secrets import compare_digest

def hash_message(data):
    '''
    returned as a string object, containing only hexadecimal digits
    >>> res1 = hash_message('yes')
    8a798890fe93817163b10b5f7bd2ca\
4d25d84c52739a645a889c173eee7d9d3d
    '''
    data = data.encode('utf-8')
    sha256_digest_1 = sha256(data)
    hexdigest = sha256_digest_1.hexdigest()
    return hexdigest


def compare_hashable_messages(hash_message1, hash_message2):
    '''
    check if hashes are equal
    >>> res1 = hash_message('hello')
    >>> res2 = hash_message('hello')
    >>> print(compare_hashable_messages(res1, res2))
    True
    '''
    return compare_digest(hash_message1, hash_message2)
