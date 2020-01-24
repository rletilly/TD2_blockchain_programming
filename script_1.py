import os, random, string ,csv

def nb_aleatoire():
    return from_bits_to_int(seed())

def seed():
    length = 132
    chars = '01'
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

def int_to_bit(integer):  #just for 11 bits blocks
    bit = str(bin(integer)).split('b')[1]
    return '0'*(11-len(bit))+bit
    
def mnemonique_to_bit(mnemonique):
    tab = mnemonique.split(' ')
    words = import_words()
    result =""
    for word in tab :
        result = result + int_to_bit(words.index(word))
    return result

#https://steemit.com/fr/@lugaxker/bitcoin-cles-privees-et-propriete
private_key = "5J3mBbAH58C"
def base58_to_hex(base58):
    result = 0
    for i in range(len(base58)):
        number = ord(base58[i])
        if number<58:
            number = number - 49
        elif number<74:
            number = number - 56
        elif number<79:
            number = number - 57
        elif number<91:
            number = number - 58
        elif number <111:
            number = number - 64
        elif number <123:
            number = number - 65
        
        result = result + number * (58**(len(base58)-1-i))
    print(result)
    result = hex(result).split('x')[1]
    return result

def base58_to_bin(base58):
    result = 0
    for i in range(len(base58)):
        number = ord(base58[i])
        if number<58:
            number = number - 49
        elif number<74:
            number = number - 56
        elif number<79:
            number = number - 57
        elif number<91:
            number = number - 58
        elif number <111:
            number = number - 64
        elif number <123:
            number = number - 65
        result = result + number * (58**(len(base58)-1-i))
    return str(bin(result)).split('b')[1]


print(base58_to_hex(private_key))










