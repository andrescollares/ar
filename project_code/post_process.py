import csv
import pandas as pd

# hay varios problemas con esto
# 1. demora mucho
# 2. la traduccion no es buena con palabras desconocidas y expresiones uruguayas
# 3. tiene un limite de request, luego de lo cual te devuelve el texto sin traducir sin avisarte nada

# from googletrans import Translator

# def transalte_en(csv_file):
#     translator = Translator()
#     # df = pd.read_csv(csv_file)
#     # print(df)
#     reader = csv.reader(csv_file)
#     next(reader, None)  # skip the headers
#     bulk_transalte = []
#     results = []

#     for index, row in enumerate(reader):
#         bulk_transalte.append(row[-1])
#         if ((index + 1) % 10 == 0):
#             translated = translator.translate(bulk_transalte, src='es', dest='en')
#             for t in translated:
#                 print(t.text)
#             results.append(bulk_transalte)
#             bulk_transalte = []


# mejor usar esto que fue entrenado sobra cosas en espanol en primer lugar

# from sentiment_analysis_spanish import sentiment_analysis
from pysentimiento import SentimentAnalyzer 

def get_sentiment(csv_file):
    analyzer = SentimentAnalyzer(lang="es")
    reader = csv.reader(csv_file)
    next(reader, None)  # skip the headers
    results = []

    for index, row in enumerate(reader):
        res = analyzer.predict(row[-1])
        # quizas es mejor no usar el atributo NEU, porque ya queda implicito en los otros 2.
        # POS + NEG + NEU = 1 siempre (son probabilidades)
        normalizado = (res.probas['POS'] - res.probas['NEG']) / (1 + res.probas['NEU'])
        print(index, '❌' if normalizado < 0 else '✔', row[-1].split('\n')[:75], normalizado)
        results.append(normalizado)
    return results

if __name__ == "__main__":
    df = pd.read_csv('data/comments.csv')
    print(df)
    with open('data/comments.csv') as f:
        results = get_sentiment(f)
    df['sentiment'] = results
    csv_string = df.to_csv(index=False, header=True)
    with open(f"data/sentiment.csv", "a") as csv:
        csv.write(csv_string)
    