import pandas as pd
import math
import modules.Person as p
from modules.filler import MAX_ALIMENTS
from matplotlib import pyplot

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
        self.factors = {'Sucres (g/100 g)': -5, 'Sel chlorure de sodium (g/100 g)': -3.5, 'AG saturés (g/100 g)': -3, 'Polyols totaux (g/100 g)': -2, 'Protéines, N x 625 (g/100 g)': 4, 'Fibres alimentaires (g/100 g)': 5}
        self.persons = {p.Person.format_codecli(nom, prenom): p.Person(nom, prenom, birth, address, postal_code, city, phone, [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]) for nom, prenom, birth, address, postal_code, city, phone, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10 in zip(self.sondage['Nom'], self.sondage['Prénom'], self.sondage['Naissance'], self.sondage['Adresse'], self.sondage['Code Postal'], self.sondage['Ville'], self.sondage['Tel'], self.sondage['Aliment1'], self.sondage['Aliment2'], self.sondage['Aliment3'], self.sondage['Aliment4'], self.sondage['Aliment5'], self.sondage['Aliment6'], self.sondage['Aliment7'], self.sondage['Aliment8'], self.sondage['Aliment9'], self.sondage['Aliment10'])}
        self.sums = self.calculate_sums() # Calculate sum of every nutrition facts per person
        self.scores = self.calculate_score() # Calculate the score (sums needed)
        self.write_excel(self.sums, "Nutrition Data")
        self.write_excel(self.scores, "HealthScore") # Write the final score using the scoring method

    def calculate_score(self):
        print("Calculating persons scores")
        df_all = pd.DataFrame()
        i = 1
        for person in self.persons.values():
            print("--> person", i)
            score = self.scoring_method(person.asHealthFrame(self.aliments))
            person_df = person.asScoreFrame(score)
            df_all = pd.concat([df_all, person_df])
            i += 1
        print("Done")
        return df_all
        
    def calculate_sums(self):
        df_all = pd.DataFrame()
        for i in self.persons.values():
            df = i.asHealthFrame(self.aliments)
            df_all = pd.concat([df_all, df])
        return df_all

    def write_excel(self, df, sheet):
        with pd.ExcelWriter("Sondage.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet, index=False)

    def scoring_method(self, person: pd.DataFrame):
        score = 0
        for k,v in self.factors.items():
            if (k == "Sucres (g/100 g)" and person[k].item() > 60):
                score += v * 1
            elif (k == "Sel chlorure de sodium (g/100 g)" and person[k].item() > 5):
                score += v * 1
            elif (k == "AG saturés (g/100 g)" and person[k].item() > 50):
                score += v * 1
            elif (k == "Polyols totaux (g/100 g)" and person[k].item() > 0):
                score += v * 1
            elif (k == "Protéines, N x 625 (g/100 g)" and person[k].item() > 100):
                score += v * 1
            elif (k == "Fibres alimentaires (g/100 g)" and person[k].item() > 28):
                score += v * 1
                
        return score

    
    def stats_healthy(self):
        statisticados = {"dead soon": 0, "not really": 0, "yes": 0, "hell yeah": 0}
        for i in self.scores["isHealthy?"]:
            statisticados[i] += 1
        return statisticados

    def show_graph_healthy(self):
        pyplot.figure(figsize = (8, 8))
        x = self.stats_healthy()
        pyplot.pie(x.values(), labels = x.keys())
        pyplot.legend()
        pyplot.show()
    

    @staticmethod
    def score_ranking(score):
        print("score ", score)
        if (score < -5):
            return "dead soon"
        elif (score < 0 and score > -5):
            return "not really"
        elif (score > 0 and score < 2):
            return "yes"
        else:
            return "hell yeah"

    @staticmethod
    #give a final score between 0 and 1.
    def sigmoid(x):
        print(x)
        return 1 / (1 + math.exp(-x))
