import random
import string


def generate_random_string(length=10):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }
