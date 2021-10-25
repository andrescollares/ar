from datetime import datetime
import sys

from crawler_praw import get_data
from graph_utils import save_graphml


# intento leer data.csv
# si existe -> creo el grafo
# si no existe -> corro el crawler
try:
    f = open('data/comments.csv', 'r')
except FileNotFoundError:
    print("Obteniendo datos...")
    get_data(limit=100)
except Exception as err:
    print(f"Unexpected error opening csv is", repr(err))
    sys.exit(1)
else:
    save_graphml(f)
