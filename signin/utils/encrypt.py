import bcrypt


def hash_string(word, salt = bcrypt.gensalt()):
    bytes = word.encode('utf-8')
    hashed = bcrypt.hashpw(bytes, salt)
    return hashed.decode('utf-8'), salt

def check_hash(input,hash):
    input_byte = input.encode('utf-8')
    hash_byte = hash.encode('utf-8')
    result = bcrypt.checkpw(input_byte, hash_byte)
    return result