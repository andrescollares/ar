import igraph as ig

# crear grafo, recibe un diccionario y guarda un graphml


def save_graphml(respuestas, name):
    respuestas_list = respuestas.items()
    users_list = [x for x, y in respuestas_list]
    edges = []
    for user, respArray in respuestas_list:
        for response_to, weight in respArray:
            edge = (user, response_to, weight)
            edges.append(edge)
    g = ig.Graph.TupleList(edges, weights=True)
    print(f"|V|={g.vcount()}, |E|={g.ecount()}")
    ig.write(g, f"{name}.graphml", "graphml")
