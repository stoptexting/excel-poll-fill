from asyncio.windows_events import NULL
from socket import SO_DEBUG
import requests
import random
import pandas as pd

url = "https://api.namefake.com/french-france/male/"
postal_codes = (76000, 76100, 76200, 76300, 76400, 76910)
cities = ("CRIEL-SUR-MER", "FLOCQUES", "ETALONDES", "LE TREPORT", "CANEHAN", "PETIT-CAUX")
sondage = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2')
aliments = pd.read_excel('Aliments.xlsx') # Read once
MAX_ALIMENTS = 10

# Person class structure
class Person:
    def __init__(self, nom, prenom, birth, address, postal_code, phone):
        self.admin = self.getAdminId()
        self.nom = nom
        self.prenom = prenom
        self.birth = birth
        self.address = address
        self.postal_code = postal_code
        self.city = self.getCity()
        self.phone = phone
        self.aliments = []
        self.code_cli = self.format_codecli()
        self.getAliments()

    def getCity(self):
        return cities[random.randrange(0, len(cities))]

    def format_codecli(self):
        return self.prenom[0:2].upper() + self.nom[0:3] if self.nom[2] != " " else self.prenom[0:2].upper() + self.nom[0:2] + self.nom[3]

    def getAliments(self):
        while len(self.aliments) != MAX_ALIMENTS:
            rand = randAlimCode()
            if (rand not in self.aliments):
                self.aliments.append(rand)

    def getAdminId(self):
        chosen = random.randint(0, 10000)
        while chosen in sondage["Administré.e"]:
            chosen = random.randint(0, 10000)
        return chosen

    def infos(self):
        print('Nom : {}\nPrenom : {}\nDate de Naissance : {}\nAddresse : {}\nCode Postal : {}\nNuméro de Téléphone : {}\n'.format(self.nom, self.prenom, self.birth, self.address, self.postal_code, self.phone))
        print("Aliments choisis :", self.aliments)
        print("Code CLI : ", self.code_cli)
        print("Admin :", self.admin)

    def asDataFrame(self):
        elements = [self.admin, self.nom, self.prenom, self.birth, self.address, self.postal_code, self.city, self.phone, self.aliments[0], self.aliments[1], self.aliments[2], self.aliments[3], self.aliments[4], self.aliments[5], self.aliments[6], self.aliments[7], self.aliments[8], self.aliments[9]]
        columns_d = list(sondage.columns.values)
        data_d = dict(zip(columns_d, elements))
        #print(data_d)
        df = pd.DataFrame([data_d])
        print(df)
        return df

# Get a random aliment code from the excel database
def randAlimCode():
    return aliments.alim_code[random.randrange(0, len(aliments.alim_code))]


# Generate a new identity
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


# Fill the Excel with a person (add on another line)
def fill_excel(p: Person):
    with pd.ExcelWriter("Sondage.xlsx", mode="a", if_sheet_exists='overlay') as writer:
        df_source = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2')
        #sondage.append(p.asDataFrame()).to_excel(writer, sheet_name="Feuil2")
        appended_df = pd.concat([df_source, p.asDataFrame()])
        appended_df.to_excel(writer, sheet_name="Feuil2")

# todo : add 10 aliments to the person, and write to the excel

def poll(n: int):
    df = NULL
    for i in range (0, n):
        p = gen_id()
        fill_excel(p)


def main(): 
    poll(10)

if __name__ == '__main__':
    main()