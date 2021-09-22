import praw
import igraph as ig
import pandas as pd

# diccionario usuario -> Array de ususarios a los que responde.
def get_data(limit = 10, save_every=10):
    reddit = praw.Reddit(
        client_id='BDKPcze-owFsIKSfxXXeJA',
        client_secret='Hj3Y2S1EhlqR3My35hameO0_kRMuxw',
        user_agent = "un cosito by ar-crawler")
    df = pd.DataFrame(columns=['commenter', 'responds_to'])
    print('asd')
    respuestas = {}
    index_submi = 0
    comment_count = 0
    for submission in reddit.subreddit("uruguay").top(limit=limit):
        submission.comments.replace_more(limit=None)
        submission_comments = submission.comments.list()
        for comment in submission_comments:
            # respuestas a post tienen prefijo t3_
            # respuestas a otros usuarios tienen prefijo t1_
            if (comment.parent_id.startswith('t3')):
                responds_to = submission.author
            else:
                parent_comment_id = comment.parent_id[3:]
                responds_to = next((x.author for x in submission_comments if x.id == parent_comment_id), None)
            # print(f"{comment.author} -> {responds_to}")
            # Usuarios eliminados dan None, filtraremos estos del dataset
            if comment.author != None and responds_to != None:
                # todo: crear el dataframe despues, par amejor performance, antes guardar en aray o dict
                df.loc[comment_count] = [comment.author, responds_to]
                # if (comment.author in respuestas):
                #     respuestas[comment.author].append(responds_to)
                # else:
                #     respuestas[comment.author] = [responds_to]
                # if (responds_to not in respuestas):
                #     respuestas[responds_to] = []
                comment_count += 1
        index_submi += 1
        print(f"Posts: {index_submi}, comentarios totales: {comment_count}")
    # guardar en CSV cada cierto tiempo (default = 10 posts)
    if index_submi % save_every == 0:
        csv_string = df.to_csv(index=False)
        with open("data.csv", "a") as csv:
            csv.write(csv_string)
        # reinicializo el dataset
        df = pd.DataFrame(columns=['commenter', 'responds_to'])




# crear grafo, recibe un diccionario
def create_graph(data):
    g = ig.Graph()
    g.add_vertices(len(respuestas))
    index = 0
    respuestas_list = respuestas.items()
    usernames = [resp[0] for resp in respuestas_list]
    g.vs["username"] = [usr.name for usr in usernames]
    for key, respArray in respuestas_list:
        for response_to in respArray:
            destination = usernames.index(response_to)
            g.add_edges([(index, destination)])
        index += 1
        

# print(g.vs["username"])
# print(df)

# ig.write(g, f"grafito-{LIMIT}.graphml", "graphml")


# print(respuestas)

