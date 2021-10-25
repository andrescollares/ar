import igraph as ig
import csv
from datetime import datetime

from constants import comment_calculated_attrs, comment_extra_attrs

def _graph_csv_to_dict(csv_file):
    with csv_file:
        reader = csv.reader(csv_file)
        respuestas = {}
        next(reader, None)  # skip the headers
        for row in reader:
            row_data = {}
            for index, key in enumerate([*comment_calculated_attrs, *comment_extra_attrs]):
                row_data[key] = row[index]
            row_data['score'] = int(row_data['score'])
            if (row_data['commenter'] in respuestas):
                try:
                    index_responds_to = [r[0]
                                         for r in respuestas[row_data['commenter']]].index(row_data['responds_to'])
                except ValueError:
                    index_responds_to = -1
                if index_responds_to >= 0:
                    # si es una respuesta repetida, aumento el peso
                    respuestas[row_data['commenter']][index_responds_to][1]['weight'] += 1
                    respuestas[row_data['commenter']][index_responds_to][1]['score'] += row_data['score']
                else:
                    # si es una nueva respuesta, creo la arista con el peso
                    respuestas[row_data['commenter']].append([row_data['responds_to'], { 'weight': 1, 'score': row_data['score'] }])
            else:
                respuestas[row_data['commenter']] = [[row_data['responds_to'], { 'weight': 1, 'score': row_data['score'] }]]
            # para usuarios que aparecen, pero no responden a nadie
            if (row_data['responds_to'] not in respuestas):
                respuestas[row_data['responds_to']] = []
    return respuestas


def save_graphml(csv_file):
    name = datetime.now().strftime("%m-%d-%Y-%H:%M")
    respuestas = _graph_csv_to_dict(csv_file)
    respuestas_list = respuestas.items()
    edges = []
    for user, respArray in respuestas_list:
        for response_to, response_dict in respArray:
            edge = (user, response_to, response_dict['weight'], response_dict['score'])
            edges.append(edge)
    g = ig.Graph.TupleList(edges, edge_attrs=['weight','score'], directed=True)
    print(f"|V|={g.vcount()}, |E|={g.ecount()}")
    ig.write(g, f"graphs/{name}.graphml", "graphml")
