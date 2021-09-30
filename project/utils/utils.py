import string
import random

def generate_random_key():
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    key = ''.join(random.choice(random_str) for i in range(12))
    return key
