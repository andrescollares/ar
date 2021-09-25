from datetime import datetime
import csv
import sys
import pandas as pd
import igraph as ig

from crawler_praw import get_data
from graph_utils import save_graphml


# intento leer data.csv
# si existe -> creo el grafo
# si no existe -> corro el crawler
try:
    f = open('data.csv', 'r')
except FileNotFoundError:
    print("Obteniendo datos...")
    get_data(limit=1000)
except Exception as err:
    print(f"Unexpected error opening data.csv is", repr(err))
    sys.exit(1)
else:
    with f:
        reader = csv.reader(f)
        respuestas = {}
        next(reader, None)  # skip the headers
        for row in reader:
            commenter, responds_to = row[0], row[1]
            if (commenter in respuestas):
                try:
                    index_responds_to = [r[0]
                                         for r in respuestas[commenter]].index(responds_to)
                except ValueError:
                    index_responds_to = -1
                if index_responds_to > 0:
                    # si es una respuesta repetida, aumento el peso en 1
                    respuestas[commenter][index_responds_to][1] += 1
                else:
                    # si es una nueva respuesta, creo la arista con peso 1
                    respuestas[commenter].append([responds_to, 1])
            else:
                respuestas[commenter] = [[responds_to, 1]]
            # para usuarios que aparecen, pero no responden a nadie
            if (responds_to not in respuestas):
                respuestas[responds_to] = []
    # df = pd.read_csv('data.csv')
    # print(df)
    # tuples = [tuple(x) for x in df.values]
    # Gm = ig.Graph.TupleList(tuples, directed = True, edge_attrs = ['is_post', 'created_utc', 'score'])
    save_graphml(respuestas, datetime.now().strftime("%m-%d-%Y-%H:%M"))
