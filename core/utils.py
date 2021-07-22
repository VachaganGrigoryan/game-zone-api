import os
import binascii


def generate_code():
    return binascii.hexlify(os.urandom(20)).decode('utf-8')
