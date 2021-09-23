import igraph as ig

# crear grafo, recibe un diccionario y guarda un graphml
def save_graphml(respuestas, name):
    g = ig.Graph()
    g.add_vertices(len(respuestas))
    index = 0
    respuestas_list = respuestas.items()
    usernames = list(respuestas.keys())
    g.vs["username"] = usernames
    for key, respArray in respuestas_list:
        for response_to in respArray:
            destination = usernames.index(response_to)
            g.add_edges([(index, destination)])
        index += 1
    print(f"|V|={g.vcount()}, |E|={g.ecount()}")
    ig.write(g, f"{name}.graphml", "graphml")