import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

def switch_operateur(argument):
    switcher = {
        'B&You': "BOUYGUES TELECOM",
        'Cdiscount': "BOUYGUES TELECOM",
        'NRJMobile': "BOUYGUES TELECOM",
        'AuchanTelecom': "BOUYGUES TELECOM",
        'BouyguesTelecom': "BOUYGUES TELECOM",
        'SFR': "SFR",
        'LaPosteMobile': "SFR",
        'RED': "SFR",
        'RegloMobile': "SFR",
        'Orange': "ORANGE",
        'Sosh': "ORANGE",
        'Syma': "ORANGE",
        'Free': 'FREE MOBILE'
    }
    return switcher.get(argument)

def comparateur():
    urlpage = 'https://lemon.fr/forfaits-mobiles-comparateur/?gclid=CjwKCAjw6qqDBhB-EiwACBs6xyIPAZk5v_DquCek6WXB4kLyDU5A9Q28h8FMLza5HI4oRKA3zHtHNRoCTz8QAvD_BwE'

    # query the website and return the html to the variable 'page'
    page = urllib.request.urlopen(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'row-offre'})

    operateur = []
    sous_operateur = []
    image = []
    forfait = []
    prix = []
    lien = []
    for result in results:
        # Récupère les opérateurs
        texte = result.find('div', attrs={'class': 'titre-h3'})
        texte = texte.find('a').getText()
        texte = texte.split(' ')
        texte = texte[0]
        # Prixtel et Coriolis sont sur les lignes Orange et SFR il faut doc les ajouter deux fois
        if texte == 'Prixtel' or texte == 'Coriolis':
            # Recupere le sous opérateur
            sous_operateur.append(texte)
            sous_operateur.append(texte)
            operateur.append('SFR')
            operateur.append('ORANGE')
            # Recupere les images
            image.append(result.find('img').get('src'))
            image.append(result.find('img').get('src'))
            # Récupère le forfait
            texte = result.find('div', attrs={'class': 'titre-h3'})
            texte = texte.find('a').getText()
            texte = texte.replace('â€“', '-').replace('–','-').split('-')
            texte = texte[1:]
            forfait.append(texte)
            forfait.append(texte)
            # Récupère le prix
            prix.append(result.find('p').getText().replace('â‚¬','€').split(' ')[1])
            prix.append(result.find('p').getText().replace('â‚¬','€').split(' ')[1])
            #Recupere le lien
            texte = result.find('div', attrs= {'class': 'd-md-none d-lg-block col-4 col-sm-2 col-link text-center'})
            lien.append(texte.find('a').get('href'))
            lien.append(texte.find('a').get('href'))
        else:
            # Recupere le sous opérateur
            sous_operateur.append(texte)
            operateur.append(switch_operateur(texte))
            # Recupere les images
            image.append(result.find('img').get('src'))
            # Récupère le forfait
            texte = result.find('div', attrs={'class': 'titre-h3'})
            texte = texte.find('a').getText()
            texte = texte.replace('â€“', '-').replace('–','-').split('-')
            texte = texte[1:]
            forfait.append(texte)
            # Récupère le prix
            prix.append(result.find('p').getText().replace('â‚¬','€').split(' ')[1])
            #Recupere le lien
            texte = result.find('div', attrs= {'class': 'd-md-none d-lg-block col-4 col-sm-2 col-link text-center'})
            lien.append(texte.find('a').get('href'))

    df = pd.DataFrame(list(zip(operateur,sous_operateur, image,forfait,prix,lien)), columns=['Opérateur', 'Sous opérateur', 'Image', 'Forfait', 'Prix', 'Lien'])
    df.to_csv('comparateur.csv', index=False)

operators = {'B&You': "BOUYGUES TELECOM", 'RED':'SFR', 'FREE': 'FREE MOBILE'}


comparateur()
df = pd.read_excel("./original.xlsx").drop('Unnamed: 0', axis= 1)
df2 = pd.read_csv("./comparateur.csv",  encoding='utf-8').rename(columns={"Opérateur": "adm_lb_nom"})

df.drop(df.loc[df['adm_lb_nom']=='BPT'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='SRR'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='ZEOP'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='ONATI'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='HUBONE'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='DIGICEL'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='TELCO OI'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='VITI SAS'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='GLOBALTEL'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='SPM TELECOM'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='MAORE MOBILE'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='PMT/VODAFONE'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='DAUPHIN TELECOM'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='OUTREMER TELECOM'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='Gouv Nelle Calédonie (OPT)'].index, inplace=True)
df.drop(df.loc[df['adm_lb_nom']=='Station étrangère'].index, inplace=True)

df[["lat", "long"]] = df["coordonnees"].str.split(", ", expand=True)
del df["coordonnees"]

df = df.merge(df2, how='inner', on='adm_lb_nom')
df["Prix"] = df["Prix"].str.replace("€", "")

df.to_csv("out.csv", encoding='utf-8')