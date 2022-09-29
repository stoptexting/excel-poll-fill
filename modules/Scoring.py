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
        self.persons = {Person.format_codecli(nom, prenom): Person(nom, prenom, birth, address, postal_code, city, phone, aliments) for nom, prenom, birth, address, postal_code, city, phone, aliments in zip(self.sondage['Nom'], self.sondage['Prénom'], self.sondage['Naissance'], self.sondage['Adresse'], self.sondage['Code Postal'], self.sondage['Ville'], self.sondage['Tel'], [self.sondage['Aliment{}'.format(i+1)] for i in range(MAX_ALIMENTS)])}
        self.calculate_score()
        #self.write_score()


    def calculate_score(self):
        df_all = pd.DataFrame()
        for i in self.persons.values():
            print(i.asDataFrame())

    def write_score(self, df):
        with pd.ExcelWriter("Sondage.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="HealthScore", index=False)

hs = HealthScore()
hs.calculate_score()
