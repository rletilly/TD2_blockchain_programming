import os, random, string ,csv, hashlib 
from Some_math_functions import *
from binascii import hexlify, unhexlify
BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

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

def bit_to_bytes(seed): # send len() that is a multiple of 8
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
    mn = from_seed_to_words(Big_seed)[0:len(from_seed_to_words(Big_seed))-1]
    return mn

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
        
def seed_to_master(mnemonique):
    seed = mnemonique_to_bit(mnemonique)
    seed = seed[0:128]
    seed = bit_to_bytes(seed)
    seed_512  = hashlib.sha512(seed).digest()
    seed_512 = bytes_to_bit(seed_512)
    Master_private_key = seed_512[0:256]
    Master_chain_code = seed_512[256:512]
    return [Master_private_key,Master_chain_code]


def publicKey(Privatekey): #Private en int
        curve = secp256k1
        result =  Math.multiply(p=curve.G,n=Privatekey,N=curve.N,A=curve.A,P =curve.P,)
        result.x = '0x'+'0'*(66-len(hex(result.x) ))+hex(result.x)[2:]
        result.y = '0x'+'0'*(66-len(hex(result.y)))+hex(result.y)[2:]
        return [result.x,result.y]


def affichage_public():
    #Module de test de la fct private key
    Privatekey = "0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD"
    Privatekey_int = int(Privatekey,16)
    Publickey = publicKey(Privatekey_int)
    print("Privatekey : " + Privatekey)
    print("")
    print("x =" + str(Publickey[0]))
    print("y =" + str(Publickey[1]))

def base58encode(hexstring):
    byteseq = bytes(unhexlify(bytes(hexstring, 'ascii')))
    n = 0
    leading_zeroes_count = 0
    for c in byteseq:
        n = n * 256 + c
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 58:
        div, mod = divmod(n, 58)
        res.insert(0, BASE58_ALPHABET[mod])
        n = div
    else:
        res.insert(0, BASE58_ALPHABET[n])

    return (BASE58_ALPHABET[0:1] * leading_zeroes_count + res).decode('ascii')

def base58decode(base58_str):
    base58_text = bytes(base58_str, "ascii")
    n = 0
    leading_zeroes_count = 0
    for b in base58_text:
        n = n * 58 + BASE58_ALPHABET.find(b)
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 256:
        div, mod = divmod(n, 256)
        res.insert(0, mod)
        n = div
    else:
        res.insert(0, n)
    return hexlify(bytearray(1) * leading_zeroes_count + res).decode('ascii')
#print(base58encode("0488B21E013442193E8000000047FDACBD0F1097043B78C63C20C34EF4ED9A111D980047AD16282C7AE6236141035A784662A4A20A65BF6AAB9AE98A6C068A81C52E4B032C0FB5400C706CFCCC56B8B9C580"))

Seed = seed()
##### Test
Seed = '000102030405060708090a0b0c0d0e0f'
Seed = int(Seed,16)
Seed = int_to_bit(Seed,128)
##### End Test
mn = mnemonique_words(Seed)

Private_key = seed_to_master(mn)[0]
Chain_code = seed_to_master(mn)[1]
PublicKey = publicKey(from_bits_to_int(Private_key))[0]



def Master_pub_Key(mn):

    Private_key = from_bits_to_int(seed_to_master(mn)[0])
    Chain_code = hex(from_bits_to_int(seed_to_master(mn)[1]))[2:]
    Chain_code = '0'*(64-len(Chain_code)) + Chain_code #On adapte la taille 
    PublicKey = publicKey(Private_key)[0][2:]
    version = "0488b21e"
    key_num = "00"
    finger_print = "00000000"
    child_number = "00000000"
    PublicKey = "02" + PublicKey
    
    Master_public = version + key_num + finger_print + child_number + Chain_code + PublicKey
    

    Master_public_bytes = int_to_bit(int(Master_public,16),624)
    Master_public_bytes =  bit_to_bytes(Master_public_bytes)
    
    hash_Master_public_bytes = hashlib.sha256(Master_public_bytes).digest()
    hash_Master_public_bytes = hashlib.sha256(hash_Master_public_bytes).digest()
    hex_check_sum = bytes_to_bit(hash_Master_public_bytes)[0:32]
    hex_check_sum = from_bits_to_int(hex_check_sum)
    hex_check_sum = hex(hex_check_sum)[2:]


    Master_public = Master_public + hex_check_sum
    Master_public = base58encode(Master_public)
    #print(Master_public)
    #TEST#
    #print(" ")
    #Response_true = 'xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8'
    #print(base58decode(Master_public))
    #print(base58decode(Response_true))
    #End test
    return Master_public
#Master_pub_Key(mn)

