import pandas as pd
import json
from graph_utils import graph_from_csv

def get_test_train():
  df = pd.read_csv('data/comments_top.csv')
  min_date = df['created_utc'].min()
  max_date = df['created_utc'].max()
  # fecha a partir de la cual partimos el conjunto en train y test
  date_cut = min_date + (max_date - min_date)/2 # "ratio" train/test
  with open('data/comments_top.csv', 'r') as data_csv:
    g = graph_from_csv(data_csv)
  g_train = g.copy()
  print(f"test: |V|={g.vcount()}, |E|={g.ecount()}")
  edges_to_delete = []
  for edge in g_train.es:
    interactions_dict = json.loads(edge['interactions'])
    edge['interactions'] = [i for i in interactions_dict if float(i['created_utc']) < date_cut]
    if not len(edge['interactions']):
      edges_to_delete.append(edge)
  g_train.delete_edges(edges_to_delete)
  print(f"train: |V|={g_train.vcount()}, |E|={g_train.ecount()}")
  return g_train, g

if __name__ == '__main__':
  get_test_train()