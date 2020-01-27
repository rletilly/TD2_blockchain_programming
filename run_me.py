from main_script import *
choix = -1
_Seed = ""
#Creation du menu :
while(choix != 'q'):
    os.system("clear") 
    print("\tTD2 Théophile Freixa & Ronan Le Tilly\n\n")
    print("Que voulez vous faire ? : \n")
    print("\t1 - Creer un entier aleatoire")
    print("\t2 - Importer une seed")
    print("\tq - Quit")

    choix = input("\nchoix ? : ")
    if choix == '1':
        os.system("clear") 
        Seed = seed()
        _Seed = Seed
        print("Notre entier aleatoire sera : \n")
        print(str(from_bits_to_int(Seed))+ "\n")
        print("Soit en binaire : \n")
        print(Seed +  "\n")
        print("Coupé en groupe de 11 : \n")
        decoupe = decoupage_11(Seed)
        for i in range(11):
            print("    " + str(i+1)+" - "+decoupe[i])
        print("    " + str(12)+" - "+Seed[121:]+ "\t\t(Il nous faut encore rajouter le chain code à l'étape suivante)")
        print(" ")
        print("Et en rajoutant le chain code on obtient la phrase : \n")
        print(mnemonique_words(Seed))
        print(" ")
        wait = input("Appuyer sur enter pour continuer")
        chois = -1
    elif choix == '2':
        while(choix != 'q'):
            os.system("clear") 
            print("Entrez votre phrase mnemonique :")
            mn = input("-> :")
            print(" ")
            if(valid_mnemonique(mn)):
                print("La seed est valide !")
            else:
                print("La seed n'est pas valide !")
            print(" ")
            print("Votre entropy est : ")
            print(" ")
            Seed = mnemonique_to_bit(mn)
            print(" Bit :"+Seed)
            Seed = from_bits_to_int(Seed)
            print(" Hex : "+ hex(Seed)[2:])
            print(" ")
            wait = input("Appuyer sur enter pour continuer")
            os.system("clear")
            a = seed_to_master(mn)
            a[0]= hex(from_bits_to_int(a[0]))
            a[1]= hex(from_bits_to_int(a[1]))
            print("Chain-code :"+a[0][2:])
            print("Private-key :"+a[1][2:])
            print(" ")
            print("On obtient la public key :")
            pub = publicKey(from_bits_to_int(seed_to_master(mn)[0]))
            print(pub)
            print(" ")
            print("Soit la extended pub key : ")
            print(Master_pub_Key(mn))
            print(" ")
            wait = input("Appuyer sur enter pour continuer")
            choix = 'q'
    elif choix == '3' :
        exit()
        
    
