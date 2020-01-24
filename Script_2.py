import os, random, string

length = 256
chars = '01'
random.seed = (os.urandom(130))

print (''.join(random.choice(chars) for i in range(length)))
