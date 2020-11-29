from py2neo import Relationship

def creation_liaison(df1,df2,item_type,item_fat,graph):

    '''

    :param df1: dataframe contenant les types d'items
    :param df2: dataframe contenant les types de matières grasses
    :param item_type: liste contenant les nodes des types d'items
    :param item_fat: liste contenant les nodes des types de matières grasses
    :param graph: la variable qui va permettre d'envoyer les relationships
    '''

    y = 0
    for c in df1.columns:
        for i in df1.index:
            if df1[c][i] == 1:
                u = 0
                for x in df2.columns:
                    if df2[x][i] == 1:
                        liaison = Relationship(item_type[y], "type", item_fat[u])
                        graph.create(liaison)
                    u = u + 1
        y = y + 1
