import os, random, string

def int_alea():
    rand = os.urandom(1)
    print(int.from_bytes(rand, byteorder='big', signed=False))
    

int_alea()
