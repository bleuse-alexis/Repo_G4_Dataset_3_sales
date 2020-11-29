from py2neo import Node
import pandas as pd

def node(df,graph,useless,var):

    '''
    :param df: le dataframe sur lequel appliquer la fonction
    :param graph: la variable qui va permettre d'envoyer les nodes
    :param useless: la liste des colonnes à supprimer
    :param var: le nom de la colonne où creer les nodes
    :return: la liste des nodes créés
    '''

    df = df.drop(useless, axis=1)
    list = []
    df=df.drop_duplicates()
    for c in df[var]:
        NODE=Node(var,name=c)
        list.append(NODE)
        graph.create(NODE)
    return list

def encoder(df,useless,var):

    '''
    :param df: dataframe où l'on récupère les données
    :param useless: liste des colonnes a supprimer
    :param var: colonne que l'on veut encoder
    :return: le dataframe avec la colonne encodé
    '''

    df = df.drop(useless, axis=1)
    one_hot = pd.get_dummies(df[var])
    df = df.drop(var, axis=1)
    df = df.join(one_hot)
    return df
