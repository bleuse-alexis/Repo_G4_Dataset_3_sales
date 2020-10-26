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

def recup_df(fileLocation):
    dfSales = pd.read_csv(fileLocation, sep="|", header=None);
    dfSales.columns = dfSales.iloc[0, :].tolist();
    dfSales = dfSales.drop(0, axis=0).reset_index(drop=True);
    return dfSales

def recup_Id(dfSales):
    ID = dfSales.loc[:, 'index'];
    return ID

def supression_colonne(dfSales):
    dfSales = dfSales.drop('index', axis=1);
    dfSales = dfSales.rename(columns={dfSales.columns[0]: "id"});
    dfSales = dfSales.drop('id', axis=1);
    dfSales = dfSales.drop(dfSales.columns[[0, 1, 2, 3, 4, 5, 6, 7]], axis=1);
    return dfSales

def modification_df(dfSales):
    # transformation des données sans rapport en 'XXXXXX'
    dfSales['Item_Identifier'] = dfSales['Item_Identifier'].astype(str)
    dfSales.loc[dfSales['Item_Identifier'] == '-400', 'Item_Identifier'] = 'XXXXX'
    dfSales.loc[dfSales['Item_Identifier'] == 'Allez au boulot ! :)', 'Item_Identifier'] = 'XXXXX'
    dfSales.loc[dfSales['Item_Identifier'] == 'nan', 'Item_Identifier'] = 'XXXXX'
    dfSales['Item_Identifier'] = dfSales.loc[:, 'Item_Identifier']

    # transformation des données non numériques en 0
    dfSales['Item_Weight'] = dfSales['Item_Weight'].astype(str)
    dfSales.loc[dfSales['Item_Weight'] == 'ù*ùfsfsf///', 'Item_Weight'] = 0.0
    dfSales.loc[dfSales['Item_Weight'] == 'nan', 'Item_Weight'] = 0.0
    dfSales['Item_Weight'] = dfSales['Item_Weight'].astype(float)

    # remplacement des valeurs 'low fat' et 'LF' en 'Low Fat' afin de réduire le nombre de catégorie
    dfSales['Item_Fat_Content'] = dfSales['Item_Fat_Content'].astype(str)
    dfSales['Item_Fat_Content'] = dfSales['Item_Fat_Content'].replace(['low fat', 'LF'], 'Low Fat')
    # remplacement des valeurs 'reg' en 'Regular'
    dfSales['Item_Fat_Content'] = dfSales['Item_Fat_Content'].replace(['reg'], 'Regular')
    # remplacement des valeurs 'nan' en 'None'
    dfSales.loc[dfSales['Item_Fat_Content'] == 'nan', 'Item_Fat_Content'] = 'None'

    # Transformation des données de la colonne en float
    dfSales['Item_Visibility'] = dfSales['Item_Visibility'].astype(float)
    # modification des lignes contenant des 0 par la moyenne
    dfSales.loc[dfSales['Item_Visibility'] == 0, 'Item_Visibility'] = dfSales.Item_Visibility.mean()

    # transformation des données de la colonne Item_MRP en float
    dfSales['Item_MRP'] = dfSales['Item_MRP'].astype(float)

    # transformation des données de la colonne Outlet_Establishment_Year en int
    dfSales['Outlet_Establishment_Year'] = dfSales['Outlet_Establishment_Year'].astype(int)

    # transformation des données de la colonne Outlet_Size en str
    dfSales['Outlet_Size'] = dfSales['Outlet_Size'].astype(str)
    # transformation des valeurs 'nan' en 'None'
    dfSales.loc[dfSales['Outlet_Size'] == 'nan', 'Outlet_Size'] = 'None'

    # transformation des données de la colonne Outlet_Location_Type en str
    dfSales['Outlet_Location_Type'] = dfSales['Outlet_Location_Type'].astype(str)

    # transformation des données de la colonne Outlet_Type en str
    dfSales['Outlet_Type'] = dfSales['Outlet_Type'].astype(str)

    # transformation des données de la colonne Item_Outlet_Sales en str
    dfSales['Item_Outlet_Sales'] = dfSales['Item_Outlet_Sales'].astype(str)
    # transformation des valeurs 'nan' en valeurs '0'
    dfSales.loc[dfSales['Item_Outlet_Sales'] == 'nan', 'Item_Outlet_Sales'] = '0'
    # retransformation des valeurs de la colonne en float et vérification des modifications
    dfSales['Item_Outlet_Sales'] = dfSales['Item_Outlet_Sales'].astype(float)
    return dfSales

def suppression_ligne(dfSales):
    # suppression des lignes contenant des 'None' celles ci ne permettant pas d'apporter d'information sur le produit
    indexname = dfSales[dfSales['Item_Fat_Content'] == 'None'].index
    dfSales.drop(indexname, inplace=True)

    #suppression des lignes contenant la valeur 'XXXXX' celles ci ne permettant pas d'identifier le produit
    indexname2=dfSales[dfSales['Item_Identifier'] == 'XXXXX' ].index
    dfSales.drop(indexname2 , inplace = True)

    # suppression des lignes contenant des 0 celles ci ne permettant pas d'apporter d'information sur le produit
    indexname3 = dfSales[dfSales['Item_Weight'] == 0].index
    dfSales.drop(indexname3, inplace=True)

    # suppression des lignes contenant des 0 celles ci ne permettant pas d'apporter d'information sur le produit
    indexname4 = dfSales[dfSales['Item_Outlet_Sales'] == 0].index
    dfSales.drop(indexname4, inplace=True)
    return dfSales

def transfo_donnees(dfSalesv2):
    # créations de colonnes permettant de trier les valeurs des colonnes étant en str avec des identifiants
    dfSalesv2.Item_Identifier = pd.Categorical(dfSalesv2.Item_Identifier)
    dfSalesv2['ID_Objet'] = dfSalesv2.Item_Identifier.cat.codes + 1
    #
    dfSalesv2.Item_Fat_Content = pd.Categorical(dfSalesv2.Item_Fat_Content)
    dfSalesv2['ID_Fat_Content'] = dfSalesv2.Item_Fat_Content.cat.codes + 1
    #
    dfSalesv2.Item_Type = pd.Categorical(dfSalesv2.Item_Type)
    dfSalesv2['ID_Item_Type'] = dfSalesv2.Item_Type.cat.codes + 1
    #
    dfSalesv2.Outlet_Identifier = pd.Categorical(dfSalesv2.Outlet_Identifier)
    dfSalesv2['ID_Outlet_Identifier'] = dfSalesv2.Outlet_Identifier.cat.codes + 1
    #
    dfSalesv2.Outlet_Size = pd.Categorical(dfSalesv2.Outlet_Size)
    dfSalesv2['ID_Outlet_Size'] = dfSalesv2.Outlet_Size.cat.codes + 1
    #
    dfSalesv2.Outlet_Location_Type = pd.Categorical(dfSalesv2.Outlet_Location_Type)
    dfSalesv2['ID_Outlet_Location_Type'] = dfSalesv2.Outlet_Location_Type.cat.codes + 1
    #
    dfSalesv2.Outlet_Type = pd.Categorical(dfSalesv2.Outlet_Type)
    dfSalesv2['ID_Outlet_Type'] = dfSalesv2.Outlet_Type.cat.codes + 1

    # suppression des colonnes en str celles ci étant remplacé par des ID
    dfSalesv2 = dfSalesv2[['ID_Objet',
                           'Item_Weight',
                           'ID_Fat_Content',
                           'Item_Visibility',
                           'ID_Item_Type',
                           'Item_MRP',
                           'ID_Outlet_Identifier',
                           'Outlet_Establishment_Year',
                           'ID_Outlet_Size',
                           'ID_Outlet_Location_Type',
                           'ID_Outlet_Type',
                           'Item_Outlet_Sales']];
    return dfSalesv2

def precision(dfSalesv2):
    # selection des colonnes qui serviront à la prédiction
    X = dfSalesv2[['ID_Objet', 'Item_Weight', 'ID_Fat_Content', 'Item_Visibility', 'ID_Item_Type', 'Item_MRP',
                   'ID_Outlet_Identifier', 'ID_Outlet_Size', 'ID_Outlet_Location_Type', 'ID_Outlet_Type',
                   'Outlet_Establishment_Year', ]]
    y = dfSalesv2['Item_Outlet_Sales']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # tentative de prédiction en régression
    randomforest = GradientBoostingRegressor(n_estimators=100, min_samples_leaf=15)
    y = dfSalesv2['Item_Outlet_Sales']
    x = dfSalesv2.loc[:, dfSalesv2.columns != 'Item_Outlet_Sales']
    # print(x)
    randomforest.fit(x, y)
    score = cross_val_score(randomforest, x, y, cv=15)
    moyenne = score.mean()
    y_predit = randomforest.predict(x)
    return moyenne