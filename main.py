# Importation des bibliothèques
import pandas as pd

from fonction.fonction_sales import recup_df
from fonction.fonction_sales import supression_colonne
from fonction.fonction_sales import modification_df
from fonction.fonction_sales import suppression_ligne
from fonction.fonction_sales import transfo_donnees
from fonction.fonction_sales import precision


# Definition des options et paramètres
pd.set_option("display.max_rows", None, "display.max_columns", None);

#emplacement fichier
fileLocation = 'Dataset_3_sales.csv';

#récupération du dataframe
df=recup_df(fileLocation)

#supression des colonnes superflu
df=supression_colonne(df)
#df.head()
#modification des données
#df=modification_df(df)

#suppression des lignes inutiles
#df=suppression_ligne(df)

#création d'un nouveau dataframe
#df2 = df

#transformation des variables str en valeurs numériques
#df2=transfo_donnees(df2)

#calcul dela precision
#moyenne=precision(df2)
#print(moyenne)
