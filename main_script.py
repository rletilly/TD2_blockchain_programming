import os, random, string

def seed():
    length = 256
    chars = '01'
    random.seed = (os.urandom(130))
    return ''.join(random.choice(chars) for i in range(length))

def decoupage_11(seed):
    pack = ""
    tab = []
    for i in range(len(seed)):
        pack = pack + seed[i]
        if((i+1)%11==0):
            tab.append(pack)
            pack =""
    return tab