# Importation des bibliothèques
import pandas as pd
import logging
from fonction.recup_csv import recup_df
from fonction.transfo_donnee import suppression_colonne
from fonction.transfo_donnee import modification_donnee
from fonction.transfo_donnee import suppression_ligne
from fonction.precision import encoder_donnee
from fonction.precision import precision

#config biblio
pd.set_option('mode.chained_assignment', None)
logging.basicConfig(filename='log.txt', level=logging.DEBUG,format='%(asctime)s %(message)s')

#emplacement fichier
fileLocation = 'Dataset_3_sales.csv'

#colonnes a supprimer

liste_ID=['index','Item_Identifier','Outlet_Identifier','Unnamed: 0',
       'Unnamed: 0.1','Unnamed: 0.1.1','Unnamed: 0.1.1.1','Unnamed: 0.1.1.1.1',
        'Unnamed: 0.1.1.1.1.1','Unnamed: 0.1.1.1.1.1.1','Unnamed: 0.1.1.1.1.1.1.1']

#valeurs a remplacer

val='0'
dico_remplacer={'low fat':'Low Fat','LF':'Low Fat','reg':'Regular','-400':'0','Allez au boulot ! :)':'0',
                'nan':'0','ù*ùfsfsf///':'0','':'0'}
logging.info('début')
val_pre='Item_Outlet_Sales'

#récupération du dataframe

df=recup_df(fileLocation)
logging.info('dataframe récupéré')

#suppression des colonnes superflu
df=suppression_colonne(df,liste_ID)
logging.info('colonnes superflus suprimés')

#modification des données
df=modification_donnee(df,dico_remplacer)
logging.info('données modifié dans le dataframe')

#suppression des lignes inutiles
df=suppression_ligne(df,val_pre,val)
logging.info('ligne suprimé')

#transformation des variables str en valeurs numériques
df=encoder_donnee(df)
logging.info('colonne str encodé')


#calcul dela precision
#result=precision(df,val_pre)
#print(result[0])

df.to_csv('data1.csv',sep=";",header=True, index=False)

logging.info('fin du programme')