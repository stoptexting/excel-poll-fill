import pandas as pd
import math
from Person import Person
from filler import MAX_ALIMENTS

# Scoring method
# 1 - Sugar & Saccharose & Glucose & Fructose (less than 25g according to studies)
# 3 - Salt
# 4 - Carbs / Fibers ratio (10:1)
# 5 - How much fibers (min 35 according to studies)
# X - Polyols
# 6 - Trans-Fats (Acides Gras Saturés)

class HealthScore:
    def __init__(self, sondage_p = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2'), aliments_df = pd.read_excel('Aliments.xlsx')) -> None:
        self.sondage = sondage_p
        self.aliments = aliments_df
        self.factors = {'sugar': -5, 'salt': -3.5, 'transfat': -3, 'polyols': -2, 'proteins': 4, 'fibers': 5}
        self.persons = {Person.format_codecli(nom, prenom): Person(nom, prenom, birth, address, postal_code, city, phone, [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]) for nom, prenom, birth, address, postal_code, city, phone, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 in zip(self.sondage['Nom'], self.sondage['Prénom'], self.sondage['Naissance'], self.sondage['Adresse'], self.sondage['Code Postal'], self.sondage['Ville'], self.sondage['Tel'], self.sondage['Aliment1'], self.sondage['Aliment2'], self.sondage['Aliment3'], self.sondage['Aliment4'], self.sondage['Aliment5'], self.sondage['Aliment6'], self.sondage['Aliment7'], self.sondage['Aliment8'], self.sondage['Aliment9'], self.sondage['Aliment10'])}
        self.scores = self.calculate_score()
        #lol = self.aliments.iloc[:, self.aliments.columns.get_loc("alim_ssssgrp_nom_fr") + 1:].columns # get nutrition facts about all products
        self.write_score(self.scores)


    def calculate_score(self):
        df_all = pd.DataFrame()
        for i in self.persons.values():
            df = i.asHealthFrame(self.aliments)
            df_all = pd.concat([df_all, df])
        return df_all

    def write_score(self, df):
        with pd.ExcelWriter("Sondage.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="HealthScore", index=False)

hs = HealthScore()
hs.calculate_score()
