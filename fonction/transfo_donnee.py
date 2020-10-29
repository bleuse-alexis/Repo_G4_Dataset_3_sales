import pandas as pd
import numpy as np
import logging
def suppression_colonne(dfSales,liste):

    logging.info('debut de fonction supression colonne')

    '''

    :param dfSales: dataframe sur lequel appliquer la fonction
    :param liste: liste des noms de colonne a supprimer
    :return: return le dataframe une fois les suppressions effectués
    '''

    dfSales = dfSales.loc[:, dfSales.columns.notnull()]
    dfSales = dfSales.drop(dfSales[liste], axis=1)
    logging.info('fin de fonction supression colonne')
    return dfSales

def modification_donnee(dfSales,liste1,liste2,liste3,val1,val2,val3):
    logging.info('debut de fonction modification donnee')
    '''

    :param dfSales: dataframe sur lequel appliquer la fonction
    :param liste1: liste des différents nom d'une des données
    :param liste2: liste des différents nom d'une des données
    :param liste3: liste des différents nom d'une des données
    :param val1: valeur remplaçante
    :param val2: valeur remplaçante
    :param val3: valeur remplaçante
    :return: return le dataframe une fois les modifications effectués
    '''
    dfSales= dfSales.astype(str)
    for c in dfSales.columns:
        for i in dfSales.index:
            for p in range(len(liste1)):
                if dfSales[c][i]==liste1[p]:
                  dfSales[c][i]=val3
            for i in range(len(liste3)):
                if dfSales[c][i]==liste2[i]:
                  dfSales[c][i]=val1
            for t in range(len(liste3)):
                if dfSales[c][i]==liste3[t]:
                  dfSales[c][i] = val2
    logging.info('fin de fonction modification donnee')
    return dfSales

def suppression_ligne(dfSales,val1,val2):
    logging.info('debut de fonction suppression ligne')

    '''

    :param dfSales: dataframe sur lequel appliquer la fonction
    :param val1: nom de la colonne a prédire
    :param val2: variable nulle a supprimer
    :return: return le dataframe une fois les lignes supprimés
    '''

    dfSales.loc[dfSales[val1]==val2,val1]=np.nan
    dfSales = dfSales.dropna(axis=0)
    for c in dfSales.columns:
        if pd.to_numeric(dfSales[c],errors='ignore').any() == True:
            dfSales[c]=dfSales[c].astype(float)
            for i in dfSales.index:
                if dfSales[c][i]==0:
                    dfSales[c][i]=dfSales[c].median()
        else:
            dfSales[c]=dfSales[c].astype(str)
            for i in dfSales.index:
                if dfSales[c][i]==val2:
                    dfSales[c][i]=np.nan
    dfSales = dfSales.dropna(axis=0)
    logging.info('fin de fonction suppression ligne')
    return dfSales