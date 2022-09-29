import pandas as pd
import matplotlib.pyplot as pyplot
from filler import MAX_ALIMENTS

class Statistics:
    def __init__(self, sondage = pd.read_excel('Sondage.xlsx', sheet_name='Feuil2'), aliments_df = pd.read_excel('Aliments.xlsx')) -> None:
        self.sondage = sondage
        self.categories_count = {"bio": 0, "vegan": 0, "casher": 0, "halal": 0, "no_categ": 0}
        self.aliments = aliments_df
        self.alimentados = {code: (group_biov, group_spe) for code, group_biov, group_spe in zip(self.aliments['alim_code'], self.aliments['alim_nom_fr'], self.aliments['alim_ssssgrp_nom_fr'])}
        self.most_chosen_categories()

    def most_chosen_categories(self):
        for i in range(MAX_ALIMENTS):
            for j in range(self.sondage.shape[0]):
                alim = self.alimentados.get(self.sondage['Aliment{}'.format(i+1)][j])
                self.categories_count[self.which_categ(alim[0], alim[1])] += 1
    
    def most_chosen_categories_tostring(self):
        output = "Categories ranking (desc.)\n"
        i = 1
        sort = {k: v for k, v in sorted(self.categories_count.items(), key=lambda item: item[1])}
        for categ_name in reversed(sort.keys()):
            output += "{}. {} with {} aliments in the list.\n".format(i, categ_name.upper(), self.categories_count.get(categ_name))
            i += 1
        return output

    def which_categ(self, group_biov_p, group_spe_p):
        if ('bio' in group_biov_p):
            return 'bio'
        elif ('vegan' in group_biov_p):
            return 'vegan'
        elif ('casher' in group_spe_p):
            return 'casher'
        elif ('halal' in group_spe_p):
            return 'halal'
        else:
            return 'no_categ'
    
    def show_graph(self):
        pyplot.figure(figsize = (8, 8))
        x = self.categories_count.values()
        pyplot.pie(x, labels = self.categories_count.keys())
        pyplot.legend()
        pyplot.show()

    

s = Statistics()
s.show_graph