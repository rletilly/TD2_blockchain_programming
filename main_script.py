import os, random, string

def seed():
    length = 256
    chars = '01'
    random.seed = (os.urandom(130))
    return ''.join(random.choice(chars) for i in range(length))
print(seed())