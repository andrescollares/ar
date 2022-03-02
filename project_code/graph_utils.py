import igraph as ig
import csv
import json
from functools import reduce
from datetime import datetime

from constants import comment_calculated_attrs, comment_extra_attrs

"""
Cada arista dirigida se representa como:
commenter: quien origina el comentario
responds_to: a quien responde
weight: cantidad de interacciones entre ambos usuarios (en ese orden)
interactions: detalle de cada interaccion (score, fecha de creacion)
"""

def _graph_csv_to_dict(csv_file):
    with csv_file:
        reader = csv.reader(csv_file)
        dictionary = {}
        next(reader, None)  # skip the headers
        for row in reader:
            row_data = {}
            for index, key in enumerate([*comment_calculated_attrs, *comment_extra_attrs]):
                row_data[key] = row[index]
            new_comment = { 'score': int(row_data['score']), 'created_utc': row_data['created_utc'] }
            if (row_data['commenter'] in dictionary):
                try:
                    index_responds_to = [r[0]
                                         for r in dictionary[row_data['commenter']]].index(row_data['responds_to'])
                except ValueError:
                    index_responds_to = -1
                if index_responds_to >= 0:
                    # si es una respuesta repetida, agrego a la lista de 'interacciones' entre los usuarios
                    dictionary[row_data['commenter']][index_responds_to][1]['response_count'] += 1
                    dictionary[row_data['commenter']][index_responds_to][1]['interactions'] += [new_comment]
                else:
                    # si es una nueva respuesta, creo la arista con el peso
                    dictionary[row_data['commenter']].append([row_data['responds_to'], { 'response_count': 1, 'interactions': [new_comment] }])
            else:
                dictionary[row_data['commenter']] = [[row_data['responds_to'], { 'response_count': 1, 'interactions': [new_comment] }]]
            # para usuarios que aparecen, pero no responden a nadie
            if (row_data['responds_to'] not in dictionary):
                dictionary[row_data['responds_to']] = []
    return dictionary

def _process_edge_attrs(response_dict):
    overall = reduce(lambda acc, elem: acc + elem['score'], response_dict['interactions'], 0)
    response_dict['positive'] = overall > 0
    response_dict['weight'] = overall
    response_dict['interactions'] = json.dumps(response_dict['interactions'])
    return response_dict

def graph_from_csv(csv_file):
    graph_data = _graph_csv_to_dict(csv_file)
    respuestas_list = graph_data.items()
    edges = []
    for user, respArray in respuestas_list:
        for response_to, response_dict in respArray:
            response_dict = _process_edge_attrs(response_dict)
            edge = (user, response_to, response_dict['weight'], response_dict['response_count'], response_dict['positive'], response_dict['interactions'])
            edges.append(edge)
    g = ig.Graph.TupleList(edges, edge_attrs=['weight', 'response_count', 'positive' ,'interactions'], directed=True)
    return g

def save_graphml(csv_file):
    name = datetime.now().strftime("%m-%d-%Y-%H:%M")
    g = graph_from_csv(csv_file)
    print(f"|V|={g.vcount()}, |E|={g.ecount()}")
    ig.write(g, f"graphs/{name}.graphml", "graphml")
