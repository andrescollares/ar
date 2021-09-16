import praw
import igraph as ig

# reddit = praw.Reddit(
#     client_id='PA80r16sX4tHy6rnYkpdyw',
#     client_secret='Tsw4ky4M2gp3l0pEbD61a2q0fOTwZQ',
#     user_agent = "crawler-ar by moy--",
#     # username = "",
#     # password = "",
# )

reddit = praw.Reddit(
    client_id='BDKPcze-owFsIKSfxXXeJA',
    client_secret='Hj3Y2S1EhlqR3My35hameO0_kRMuxw',
    user_agent = "un cosito by ar-crawler",
    # username = "",
    # password = "",
)

# print(reddit.read_only)

# diccionario usuario -> Array de ususarios a los que responde.
respuestas = {}

for submission in reddit.subreddit("uruguay").top(limit=200):
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
        print(f"{comment.author} -> {responds_to}")
        # Algunos dan none, no se por que
        if comment.author != None and responds_to != None:
            if (comment.author in respuestas):
                respuestas[comment.author].append(responds_to)
            else:
                respuestas[comment.author] = [responds_to]
            if (responds_to not in respuestas):
                respuestas[responds_to] = []
        
        # crear grafo
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
        

print(g.vs["username"])

ig.write(g, "grafito-200.graphml", "graphml")

        

# print(respuestas)

