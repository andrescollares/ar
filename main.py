from datetime import datetime
import sys
import pandas as pd
import igraph as ig

from crawler_praw import get_data
from graph_utils import graph_csv_to_dict, save_graphml


# intento leer data.csv
# si existe -> creo el grafo
# si no existe -> corro el crawler
try:
    f = open('data/data.csv', 'r')
except FileNotFoundError:
    print("Obteniendo datos...")
    get_data(limit=10)
except Exception as err:
    print(f"Unexpected error opening data.csv is", repr(err))
    sys.exit(1)
else:
    respuestas = graph_csv_to_dict(f)
    save_graphml(respuestas, datetime.now().strftime("%m-%d-%Y-%H:%M"))
