import random
import pandas as pd
import time

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
    
    def asHealthFrame(self, aliments_df):
        elements = [self.code_cli, self.nom, self.prenom, self.birth, self.address, self.postal_code, self.city, self.phone, self.aliments[0], self.aliments[1], self.aliments[2], self.aliments[3], self.aliments[4], self.aliments[5], self.aliments[6], self.aliments[7], self.aliments[8], self.aliments[9]]
        columns_d = list(sondage.columns.values)
        columns_d.insert(0, "Code_CLI")
        columns_d.remove('Administré.e')
        columns_d.extend(['Sucres (g/100 g)', 'Sel chlorure de sodium (g/100 g)', 'AG saturés (g/100 g)', 'Polyols totaux (g/100 g)', 'Protéines, N x 625 (g/100 g)', 'Fibres alimentaires (g/100 g)'])

        nutrisum = self.sumNutritionFacts(aliments_df)
        # print(nutrisum)
        elements.extend(nutrisum) # ok

        data_d = dict(zip(columns_d, elements))
        df = pd.DataFrame([data_d])
        return df


    # Scoring method
    # 1 - Sugar
    # 3 - Salt
    # 4 - How much fibers (min 35 according to studies)
    # 5 - Polyols
    # 6 - Trans-Fats (Acides Gras Saturés)
    def sumNutritionFacts(self, aliments_df):
        sugar = 0
        salt = 0
        transfat = 0
        polyols = 0
        proteins = 0
        fibers = 0

        for alim in self.aliments:
            alim_row = aliments_df.loc[aliments_df['alim_code'] == alim]
            alim_row = alim_row[['Sucres (g/100 g)', 'Sel chlorure de sodium (g/100 g)', 'AG saturés (g/100 g)', 'Polyols totaux (g/100 g)', 'Protéines, N x 625 (g/100 g)', 'Fibres alimentaires (g/100 g)']]
            alim_row = alim_row.stack().str.replace(',', '.', regex=True).str.replace('[A-Za-z]', '', regex=True).str.replace('[-]', '0', regex=True).str.replace('[< ]', '', regex=True).str.replace('^$', '0', regex=True).unstack()
            alim_row.apply(lambda x: x.replace(',','.'))
            sugar += float(0.0 if 'Sucres (g/100 g)' not in alim_row.keys() else alim_row['Sucres (g/100 g)'])
            salt += float(0.0 if 'Sel chlorure de sodium (g/100 g)' not in alim_row.keys() else alim_row['Sel chlorure de sodium (g/100 g)'])
            transfat += float(0.0 if 'AG saturés (g/100 g)' not in alim_row.keys() else alim_row['AG saturés (g/100 g)'])
            polyols += float(0.0 if 'Polyols totaux (g/100 g)' not in alim_row.keys() else alim_row['Polyols totaux (g/100 g)'])
            proteins += float(0.0 if 'Protéines, N x 625 (g/100 g)' not in alim_row.keys() else alim_row['Protéines, N x 625 (g/100 g)'])
            fibers += float(0.0 if 'Fibres alimentaires (g/100 g)' not in alim_row.keys() else alim_row['Fibres alimentaires (g/100 g)'])
        return [sugar, salt, transfat, polyols, proteins, fibers]


    def asScoreFrame(self, score):
        elements = [self.code_cli, self.nom, self.prenom, self.birth, self.address, self.postal_code, self.city, self.phone, score]
        columns_d = list(sondage.columns.values)
        columns_d.insert(0, "Code_CLI")
        columns_d.remove('Administré.e')
        columns_d = [x for x in columns_d if "Aliment" not in x]
        columns_d.extend(['Final Score', 'isHealthy?'])

        from modules.Scoring import HealthScore as h # https://stackoverflow.com/questions/7199466/how-to-break-import-loop-in-python
        isHealthy = h.score_ranking(score)
        elements.append(isHealthy)

        data_d = dict(zip(columns_d, elements))
        df = pd.DataFrame([data_d])
        return df

    




