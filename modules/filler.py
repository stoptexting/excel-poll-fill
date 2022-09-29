import random
import pandas as pd
from Person import Person
from Aliments import Classes

persons = pd.read_excel('Persons.xlsx', sheet_name='Persons')
postal_codes = (76910, 76260, 76270, 76470, 76400, 76370)
cities = ("CRIEL-SUR-MER", "FLOCQUES", "ETALONDES", "LE TREPORT", "CANEHAN", "PETIT-CAUX")
#aliments = pd.read_excel('Aliments.xlsx') # Read once
aliments_list = Classes()
MAX_ALIMENTS = 10

# Generate a new identity
def gen_id(categ):
    if (categ not in ['bio', 'vegan', 'casher', 'halal', 'no_categ']):
        raise "category does not exist. available categories : vegan, bio, casher, halal or no_categ."

    nom = persons["Nom"][random.randrange(0, len(persons["Nom"]))]
    prenom = persons["Prénom"][random.randrange(0, len(persons["Prénom"]))]
    birth = persons["Naissance"][random.randrange(0, len(persons["Naissance"]))]
    address = persons["Adresse"][random.randrange(0, len(persons["Adresse"]))]
    postal_code = postal_codes[random.randrange(0, len(postal_codes))]
    city = cities[random.randrange(0, len(cities))]
    phone = persons["Tel"][random.randrange(0, len(persons["Tel"]))]
    aliments = aliments_list.random_by_class(categ, MAX_ALIMENTS)
    
    return Person(nom, prenom, birth, address, postal_code, city, phone, aliments)

# Fill the Excel with a person (add on another line)
# df : dataframe with every entries
def fill_excel(df):
    with pd.ExcelWriter("Sondage.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="Feuil2", index=False)

def poll(n: int):
    df_all = pd.DataFrame()
    for i in range (0, n):
        rand = random.random()
        categ = "no_categ" # 60%
        if (rand >= 0.60 and rand < 0.75):
            categ = "bio" # 15%
        elif (rand >= 0.75 and rand < 0.85):
            categ = "vegan" # 10%
        elif (rand >= 0.85 and rand < 0.95):
            categ = "casher" # 10%
        elif (rand >= 0.95 and rand < 1.0):
            categ = "halal" # 5%
        else:
            categ = "no_categ" # still 60%, just in case

        p = gen_id(categ)
        print("Generating Person", i + 1, ": it's a", categ, "eater.")
        df = p.asDataFrame()
        df_all = pd.concat([df_all, df])
    fill_excel(df_all)
