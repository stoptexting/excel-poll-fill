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
            print("--------------- alim avant replace ", alim, " ", alim_row.values)
            # if regex not here, replace not working!!!!!!!!!!!!
            alim_row = alim_row.stack().str.replace(',', '.', regex=True).str.replace('[A-Za-z]', '', regex=True).str.replace('[-]', '0', regex=True).str.replace('[< ]', '', regex=True).str.replace('^$', '0', regex=True).unstack()
            print("-------------- alim après replace", alim, " ", alim_row.values)
            #print(alim_row)
            # Scoring method
            # 1 - Sugar
            # 3 - Salt
            # 4 - How much fibers (min 35 according to studies)
            # 5 - Polyols
            # 6 - Trans-Fats (Acides Gras Saturés)
            # self.factors = {'sugar': -5, 'salt': -3.5, 'transfat': -3, 'polyols': -2, 'proteins': 4, 'fibers': 5}
            # print([sugar, salt, transfat, polyols, proteins, fibers])
            #print(alim_row.columns.values)
            alim_row.apply(lambda x: x.replace(',','.'))
            print("before", [sugar, salt, transfat, polyols, proteins, fibers])
            print("alim", alim, " ", alim_row.values)
            sugar += float(0.0 if 'Sucres (g/100 g)' not in alim_row.keys() else alim_row['Sucres (g/100 g)'])
            salt += float(0.0 if 'Sel chlorure de sodium (g/100 g)' not in alim_row.keys() else alim_row['Sel chlorure de sodium (g/100 g)'])
            transfat += float(0.0 if 'AG saturés (g/100 g)' not in alim_row.keys() else alim_row['AG saturés (g/100 g)'])
            polyols += float(0.0 if 'Polyols totaux (g/100 g)' not in alim_row.keys() else alim_row['Polyols totaux (g/100 g)'])
            proteins += float(0.0 if 'Protéines, N x 625 (g/100 g)' not in alim_row.keys() else alim_row['Protéines, N x 625 (g/100 g)'])
            fibers += float(0.0 if 'Fibres alimentaires (g/100 g)' not in alim_row.keys() else alim_row['Fibres alimentaires (g/100 g)'])
            print("after", [sugar, salt, transfat, polyols, proteins, fibers])

        # df_all = pd.DataFrame()
        # for alim in self.aliments:
        #     # print(self.aliments)
        #     # print("alim", alim)
        #     alim_row = aliments_df.loc[aliments_df['alim_code'] == alim]
        #     # print(alim_row)
        #     nutri_facts = alim_row.iloc[:, alim_row.columns.get_loc("alim_ssssgrp_nom_fr") + 1:]
        #     #print(nutri_facts)
        #     df_all = pd.concat([df_all, nutri_facts])
        # # print("dfall", df_all)

        # nutrifactados_list = []
        # for col in aliments_df.iloc[:, aliments_df.columns.get_loc("alim_ssssgrp_nom_fr") + 1:].columns.values.tolist():
        #     df_all[col] = [float(str(i).replace("-", "0").replace(",", "").replace("traces", "0").replace("<", "")) for i in df_all[col]]
        #     print(df_all[col].sum())
        #     print(df_all[col].values)
        #     nutrifactados_list.append(df_all[col].sum())
        # # print(nutrifactados_list)

        # ''' bug vient du fait que en float ça met des 0 partout
        # alim avant replace  40057   [[40057 'Coeur, dinde, cuit' nan 4 'viandes, œufs, poissons et assimilés'
        # 401 'viandes cuites' 40108 'abats halal' '701' '167' '701' '167' '67,2'
        # '24,9' '24,9' '0' '7,52' '0' '-' '-' '-' '-' '-' '-' '-' '0' '0' '1,21'
        # '0' 'traces' '1,9' '1,67' '1,83' '0' '0' '0' '0,004' '0,054' '0,064'
        # '1,12' '0,63' '1,48' '1,39' '0,049' '-' '0,009' '0,005' '359' '0,35'
        # '21' '-' '0,83' '6,96' '-' '28' '0,12' '241' '203' '-' '140' '4,6' '16'
        # '0' '0' '0,13' '0' '-' '-' '0,24' '1,54' '7,76' '1,58']]
        # before [0.0, 0.0815, 110.301, 0.0, 9140.06, 0.0]
        # alim 40057   [['000' '000.03050' '010.090' '000' '02040.090' '000']]
        # after [0.0, 0.112, 120.391, 0.0, 11180.15, 0.0]
        # '''

        print([sugar, salt, transfat, polyols, proteins, fibers])
        return [sugar, salt, transfat, polyols, proteins, fibers]


