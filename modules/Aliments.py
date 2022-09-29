import pandas as pd
import random
import os

class Classes:
    def __init__(self, aliments_df = pd.read_excel('Aliments.xlsx')) -> None:
        self.aliments = aliments_df
        self.classes = {"bio": [], "vegan": [], "casher": [], "halal": [], "no_categ": []}
        self.fill_classes()

    # groupe_bio : is bio/vegan or not, groupe_spe : others
    def fill_classes(self):
        print("Sorting aliments per category...")
        alimentados = [(code, group_biov, group_spe) for code, group_biov, group_spe in zip(self.aliments['alim_code'], self.aliments['alim_nom_fr'], self.aliments['alim_ssssgrp_nom_fr'])]
        for code, group_biov, group_spe in alimentados:
            if ('bio' in group_biov):
                self.classes["bio"].append(code)
            elif ('vegan' in group_biov):
                self.classes["vegan"].append(code)
            elif ('casher' in group_spe):
                self.classes["casher"].append(code)
            elif ('halal' in group_spe):
                self.classes["halal"].append(code)
            else:
                self.classes["no_categ"].append(code)
        print("Done")

    # Only a certain class of aliments, categ : the category
    def random_by_class(self, categ: str, n: int):
        aliments = []
        categ = categ.lower()
        if (categ not in self.classes.keys()):
            raise "category does not exist. available categories : vegan, bio, casher, halal or no_categ."

        while len(aliments) != n:
            rand = self.classes[categ][random.randrange(0, len(self.classes[categ]))]
            if (rand not in aliments):
                aliments.append(rand)
        return aliments

    # Mixed results, only vegan, bio and aliments without group
    def random(self, n: int):
        aliments = []
        allowed = ['vegan', 'bio', 'no_categ']
        while len(aliments) != n:
            categ = allowed[random.randrange(0, len(allowed))]
            rand = self.classes[categ][random.randrange(0, len(self.classes[categ]))]
            if (rand not in aliments):
                aliments.append(rand)
        return aliments