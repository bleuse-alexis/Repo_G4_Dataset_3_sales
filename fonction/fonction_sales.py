import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
def recup_df(fileLocation):
    dfSales = pd.read_csv(fileLocation, sep="|", header=None);
    dfSales.columns = dfSales.iloc[0, :].tolist();
    dfSales = dfSales.drop(0, axis=0).reset_index(drop=True);
    return dfSales

def supression_colonne(dfSales):
    dfSales = dfSales.loc[:, dfSales.columns.notnull()]
    dfSales = dfSales.drop('Item_Identifier', axis=1)
    dfSales = dfSales.drop('Outlet_Identifier', axis=1)
    for c in dfSales.columns:
        if '1' == dfSales[c][1]:
            dfSales = dfSales.drop(dfSales[[c]], axis=1)
        elif '1.0'==dfSales[c][1]:
            dfSales = dfSales.drop(dfSales[[c]], axis=1)
    return dfSales

def modification_df(dfSales):

    dfSales= dfSales.astype(str)
    for c in dfSales.columns:
        for i in dfSales.index:
            if dfSales[c][i]=='-400':
               dfSales[c][i]='0'
            elif dfSales[c][i]=='Allez au boulot ! :)':
                dfSales[c][i]='0'
            elif dfSales[c][i]=='nan':
                dfSales[c][i]='0'
            elif dfSales[c][i]=='ù*ùfsfsf///':
                dfSales[c][i]='0'
            elif dfSales[c][i]=='low fat':
                dfSales[c][i]='Low Fat'
            elif dfSales[c][i]=='LF':
                dfSales[c][i]='Low Fat'
            elif dfSales[c][i]=='reg':
                dfSales[c][i]='Regular'
            elif dfSales[c][i]=='':
                dfSales[c][i]='0'
    return dfSales



def suppression_ligne(dfSales):

    dfSales.loc[dfSales['Item_Outlet_Sales']=='0','Item_Outlet_Sales']=np.nan
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
                if dfSales[c][i]=='0':
                    dfSales[c][i]=np.nan
    dfSales = dfSales.dropna(axis=0)
    return dfSales



def transfo_donnees(dfSales):
    col_groups = dfSales.columns.to_series().groupby(dfSales.dtypes).groups
    str_list = col_groups[np.dtype('O')]
    dfSales2=pd.get_dummies(dfSales[str_list])
    dfSales=dfSales.join(dfSales2)
    dfSales=dfSales.drop(str_list,axis=1)

    return dfSales



def precision(dfSales):

    # tentative de prédiction en régression
    randomforest = GradientBoostingRegressor(n_estimators=100, min_samples_leaf=15)
    y = dfSales['Item_Outlet_Sales']
    x = dfSales.loc[:, dfSales.columns != 'Item_Outlet_Sales']
    randomforest.fit(x, y)
    score = cross_val_score(randomforest, x, y, cv=15)
    moyenne = score.mean()
    y_predit = randomforest.predict(x)
    return moyenne