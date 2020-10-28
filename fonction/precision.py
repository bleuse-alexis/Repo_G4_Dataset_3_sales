import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
import logging



def encoder_donnee(dfSales):
    logging.info('debut de la fonction encoder donnee')

    '''

    :param dfSales: dataframe sur lequel appliquer la fonction
    :return: return du dataframe une fois les valeurs str encodés
    '''

    col_groups = dfSales.columns.to_series().groupby(dfSales.dtypes).groups
    str_list = col_groups[np.dtype('O')]
    dfSales2=pd.get_dummies(dfSales[str_list])
    dfSales=dfSales.join(dfSales2)
    dfSales=dfSales.drop(str_list,axis=1)
    logging.info('fin de la fonction encoder donnee')
    return dfSales



def precision(dfSales,var):
    logging.info('debut de la fonction precision')

    '''

    :param dfSales: dataframe sur lequel appliquer la fonction
    :param var: nom de la colonne a prédire
    :return: return la moyenne de précision ainsi que les predictions effectués
    '''

    # tentative de prédiction en régression
    randomforest = GradientBoostingRegressor(n_estimators=100, min_samples_leaf=15)
    y = dfSales[var]
    x = dfSales.loc[:, dfSales.columns != var]
    randomforest.fit(x, y)
    score = cross_val_score(randomforest, x, y, cv=15)
    moyenne = score.mean()
    y_predit = randomforest.predict(x)
    logging.info('fin de la fonction precision')
    return moyenne,y_predit
