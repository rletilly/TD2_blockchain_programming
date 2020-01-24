import os, random, string

length = 132
chars = '01'
random.seed = (os.urandom(256))
seed_binaire = ''.join(random.choice(chars) for i in range(length))
print(len(seed_binaire))
print(seed_binaire)
tab = [0]*12
for j in range(0,12):
    tab[j] = seed_binaire[j:j+11]
    print(tab[j])
