import pandas as pd
import logging
def recup_df(fileLocation):


    '''

    :param fileLocation: nom du fichier a récupérer
    :return: return un dataframe tiré du fichier

    '''

    logging.info('début fonction recup')

    dfSales = pd.read_csv(fileLocation, sep="|", header=None)
    dfSales.columns = dfSales.iloc[0, :].tolist()
    dfSales = dfSales.drop(0, axis=0).reset_index(drop=True)
    logging.info('fin de fonction récup')
    return dfSales
