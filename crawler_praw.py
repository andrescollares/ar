import praw
import pandas as pd
import pprint

from datetime import datetime
from graph_utils import save_graphml
from constants import comment_calculated_attrs, comment_extra_attrs, post_attrs_columns

def _commentsDataFrame():
    return pd.DataFrame(
        columns=[*comment_calculated_attrs, *comment_extra_attrs])

def _postsDataFrame():
    return pd.DataFrame(columns=post_attrs_columns)

def _saveDataCsv(name, df, write_header):
    csv_string = df.to_csv(index=False, header=write_header)
    with open(f"data/{name}.csv", "a") as csv:
        csv.write(csv_string)



def get_data(limit=10, save_every=10):
    reddit = praw.Reddit(
        client_id='BDKPcze-owFsIKSfxXXeJA',
        client_secret='Hj3Y2S1EhlqR3My35hameO0_kRMuxw',
        user_agent="un cosito by ar-crawler")
    df_comments = _commentsDataFrame()
    index_submi = 0
    comment_count = 0
    df_posts = _postsDataFrame()
    for submission in reddit.subreddit("uruguay").top(time_filter="year", limit=limit):
        submission_id = submission.id
        post_attrs = [getattr(submission, key) for key in post_attrs_columns]
        df_posts.loc[df_posts.shape[0]] = post_attrs
        submission.comments.replace_more(limit=None)
        submission_comments = submission.comments.list()
        for comment in submission_comments:
            # pprint.pprint(vars(comment))
            # respuestas a post tienen prefijo t3_
            # respuestas a otros usuarios tienen prefijo t1_
            is_root_comment = comment.parent_id.startswith('t3')
            if (is_root_comment):
                responds_to = submission.author
            else:
                parent_comment_id = comment.parent_id[3:]
                responds_to = next(
                    (x.author for x in submission_comments if x.id == parent_comment_id), None)
            # Usuarios eliminados dan None, filtraremos estos del dataset
            if comment.author != None and responds_to != None:
                # todo: crear el dataframe despues, par amejor performance, antes guardar en aray o dict
                calculated_attrs = [comment.author, responds_to, is_root_comment, submission_id]
                extra_attrs = [getattr(comment, key) for key in comment_extra_attrs]
                df_comments.loc[df_comments.shape[0]] = [*calculated_attrs, *extra_attrs]
                comment_count += 1
        index_submi += 1
        print(f"Posts: {index_submi}, comentarios totales: {comment_count}")
        # guardar en CSV cada cierto tiempo (default = 10 posts)
        if index_submi % save_every == 0:
            _saveDataCsv('comments', df_comments, index_submi == save_every)
            _saveDataCsv('posts', df_posts, index_submi == save_every)
            utc_date = df_comments.iloc[-1:]['created_utc']
            print(f'Ultimo comentario: {datetime.utcfromtimestamp(utc_date).strftime("%Y/%m/%d")}')
            df_comments = _commentsDataFrame()
            df_posts = _postsDataFrame()
    with open('data/comments.csv', 'r') as csv:
        save_graphml(csv)
