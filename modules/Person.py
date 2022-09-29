import random
import pandas as pd

url = "https://api.namefake.com/french-france/male/"
sondage = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2')
MAX_ADMIN = 1000000

# Person class structure
class Person:
    def __init__(self, nom, prenom, birth, address, postal_code, city, phone, aliments):
        self.admin = self.getAdminId()
        self.nom = nom
        self.prenom = prenom
        self.birth = birth
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.phone = phone
        self.aliments = aliments
        self.code_cli = self.format_codecli(self.nom, self.prenom)
        
    @staticmethod
    def format_codecli(nom, prenom):
        return prenom[0:2].upper() + nom[0:3] if nom[2] != " " else prenom[0:2].upper() + nom[0:2] + nom[3]

    def getAdminId(self):
        chosen = random.randint(0, MAX_ADMIN)
        while chosen in sondage["Administré.e"]:
            chosen = random.randint(0, MAX_ADMIN)
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
        df = pd.DataFrame([data_d])
        return df

