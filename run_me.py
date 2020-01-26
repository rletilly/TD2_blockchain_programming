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
        print("    " + str(12)+" - "+Seed[121:])
        print(" ")
        print("Et en rajoutant le chain code on obtient la phrase : \n")
        print(mnemonique_words(Seed))
        print(" ")
        wait = input("Appuyer sur enter pour continuer")
        chois = -1
    elif choix == '2':
        while(choix != 'q'):
            print("a")
    elif choix == '3' :
        exit()
    
