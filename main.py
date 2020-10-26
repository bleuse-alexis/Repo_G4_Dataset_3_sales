# Importation des bibliothèques
import pandas as pd
import numpy as np
import math
import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from fonction_sales import recup_df
from fonction_sales import recup_Id
from fonction_sales import supression_colonne
from fonction_sales import modification_df
from fonction_sales import suppression_ligne
from fonction_sales import transfo_donnees
from fonction_sales import precision


# Definition des options et paramètres
pd.set_option("display.max_rows", None, "display.max_columns", None);

#emplacement fichier
fileLocation = 'Dataset_3_sales.csv';

#récupération du dataframe
df=recup_df(fileLocation)

#récupération de l'ID
ID_df=recup_Id(df)

#supression des colonnes superflu
df=supression_colonne(df)

#modification des données
df=modification_df(df)

#suppression des lignes inutiles
df=suppression_ligne(df)

#création d'un nouveau dataframe
df2 = df

#transformation des variables str en valeurs numériques
df2=transfo_donnees(df2)

#calcul dela precision
moyenne=precision(df2)
print(moyenne)
