import igraph as ig
import csv

# crear grafo, recibe un diccionario y guarda un graphml


def graph_csv_to_dict(csv_file):
    with csv_file:
        reader = csv.reader(csv_file)
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
    return respuestas


def save_graphml(respuestas, name):
    respuestas_list = respuestas.items()
    edges = []
    for user, respArray in respuestas_list:
        for response_to, weight in respArray:
            edge = (user, response_to, weight)
            edges.append(edge)
    g = ig.Graph.TupleList(edges, weights=True)
    print(f"|V|={g.vcount()}, |E|={g.ecount()}")
    ig.write(g, f"data/{name}.graphml", "graphml")
