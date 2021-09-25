from datetime import datetime
import csv
import sys
import pandas as pd

from crawler_praw import get_data
from graph_utils import save_graphml


# intento leer data.csv
# si existe -> creo el grafo
# si no existe -> corro el crawler
try:
    f = open('data.csv', 'r')
except FileNotFoundError:
    print("Obteniendo datos...")
    get_data(limit=10)
except Exception as err:
    print(f"Unexpected error opening data.csv is",repr(err))
    sys.exit(1)
else:
    with f:
        df = pd.read_csv('data.csv')
        print(df)
    #     reader = csv.reader(f)
    #     respuestas = {}
    #     for row in reader:
    #         print(row)
    #         commenter, responds_to = row
    #         if (commenter in respuestas):
    #             respuestas[commenter].append(responds_to)
    #         else:
    #             respuestas[commenter] = [responds_to]
    #         if (responds_to not in respuestas):
    #             respuestas[responds_to] = []
    # save_graphml(respuestas, datetime.now().strftime("%m-%d-%Y-%H:%M"))

        