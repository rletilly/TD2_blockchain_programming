import os, random, string ,csv, hashlib

def nb_aleatoire():
    return from_bits_to_int(seed())

def seed():
    return bytes_to_bit(os.urandom(16))
def decoupage_11(seed):
    pack = ""
    tab = []
    for i in range(len(seed)):
        pack = pack + seed[i]
        if((i+1)%11==0):
            tab.append(pack)
            pack =""
    return tab

def from_bits_to_int(bits):
    result = 0
    for i in range(len(bits)):
        result =result + int(bits[i]) * (2**(len(bits)-1-i))
    return(result)

def import_words():
    words_BIP39 = []
    with open('Words_BIP39.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            words_BIP39.append(row[0])
    return words_BIP39

def from_seed_to_words(seed):
    words = import_words()
    tab = decoupage_11(seed)
    result = ""
    for pack in tab :
        result = result +words[from_bits_to_int(pack)] + " "
    return result

def int_to_bit(integer,size):
    bit = str(bin(integer)).split('b')[1]
    return '0'*(size-len(bit))+bit
    
def mnemonique_to_bit(mnemonique):
    tab = mnemonique.split(' ')
    words = import_words()
    result =""
    for word in tab :
        result = result + int_to_bit(words.index(word),11)
    return result


def bytes_to_bit(seed): 
    response =''
    for i in range(len(seed)):
        response = response + int_to_bit(seed[i],8)
    return response

def bit_to_bytes(seed):
    first_loop = True
    pack = ""
    for i in range(len(seed)):
        pack = pack + seed[i]
        if((i+1)%8==0):
            if(first_loop ==  False):
                tab = tab+bytes([from_bits_to_int(pack)])
            else :
                tab = bytes([from_bits_to_int(pack)])
                first_loop = False
            pack =""
    return tab


def mnemonique_words(seed): #seed must be binary
    seed_bytes = bit_to_bytes(seed)
    hash_seed_bytes = hashlib.sha256(seed_bytes).digest()
    hash_seed_bits = bytes_to_bit(hash_seed_bytes)
    four_first_bits = hash_seed_bits[0] + hash_seed_bits[1] + hash_seed_bits[2] + hash_seed_bits[3]
    Big_seed = seed + four_first_bits
    return from_seed_to_words(Big_seed)

def valid_mnemonique(mnemonique):
    Big_seed = mnemonique_to_bit(mnemonique)
    seed=''
    for i in range(len(Big_seed)-4):
        seed = seed + Big_seed[i]
    chain_code =Big_seed[128]+ Big_seed[129]+ Big_seed[130]+ Big_seed[131]
    #Now we got seed + chain code
    seed_bytes = bit_to_bytes(seed)
    hash_seed_bytes = hashlib.sha256(seed_bytes).digest()
    hash_seed_bits = bytes_to_bit(hash_seed_bytes)
    four_first_bits = hash_seed_bits[0] + hash_seed_bits[1] + hash_seed_bits[2] + hash_seed_bits[3]
    if four_first_bits == chain_code:
        return True
    else:
        return False