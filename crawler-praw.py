import praw

reddit = praw.Reddit(
    client_id='PA80r16sX4tHy6rnYkpdyw',
    client_secret='Tsw4ky4M2gp3l0pEbD61a2q0fOTwZQ',
    user_agent = "crawler-ar by moy--",
    # username = "",
    # password = "",
)

# print(reddit.read_only)

for submission in reddit.subreddit("uruguay").hot(limit=10):
    print(submission.title)
