import requests
import random
import pandas as pd

url = "https://api.namefake.com/french-france/male/"
postal_codes = (76000, 76100, 76200, 76300, 76400, 76910)
sondage = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2')
aliments = pd.read_excel('Aliments.xlsx') # Read once

class Person:
    def __init__(self, nom, prenom, birth, address, postal_code, phone):
        self.nom = nom
        self.prenom = prenom
        self.birth = birth
        self.address = address
        self.postal_code = postal_code
        self.phone = phone

    def infos(self):
        print('Nom : {}\nPrenom : {}\nDate de Naissance : {}\nAddresse : {}\nCode Postal : {}\nNuméro de Téléphone : {}\n'.format(self.nom, self.prenom, self.birth, self.address, self.postal_code, self.phone))


def randAlimCode():
    return aliments.alim_code[random.randrange(0, len(aliments.alim_code))]

def gen_id():
    data = requests.get(url)
    data = data.json()
    nom = data["name"].split(" ")[1].upper() + data["name"].split(" ")[len(data["name"].split(" ")) - 1].upper() if len(data["name"].split(" ")) > 2 else data["name"].split(" ")[1].upper()
    prenom = data["name"].split(" ")[0]
    birth = data["birth_data"]
    address = data["address"].split("\n")[0]
    postal_code = postal_codes[random.randrange(0, len(postal_codes))]
    phone = data["phone_h"]
    
    return Person(nom, prenom, birth, address, postal_code, phone)



def main():
    print("lol rand", randAlimCode())
    p = gen_id()
    print(p.infos())


if __name__ == '__main__':
    main()










