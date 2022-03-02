import praw

reddit = praw.Reddit( client_id='PA80r16sX4tHy6rnYkpdyw', client_secret='Tsw4ky4M2gp3l0pEbD61a2q0fOTwZQ', user_agent = "crawler-ar by moy--",)

subreddit = reddit.subreddit("uruguay") # <- conseguir un subreddit

subreddit.display_name

subreddit.title

for submission in subreddit.hot(limit=10): # <- recorrer los posts
    submission.author # <- el autor
    submission.title # <- el título
    submission.score

    # submission.comment_sort = "top" <- permite ordenar
    submission.comments.list()

redditor = reddit.redditor("moy--") # <- como conseguir un usuario
redditor.link_karma
redditor.comment_karma
redditor.name
redditor.comments

redditor.subreddits # <- subreddits en los que participa

