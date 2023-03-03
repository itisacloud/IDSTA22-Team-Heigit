from entityRecognition import entityModel
from sentiment import sentimentModel
from connections import elasticSearchConnection as es

from os.path import join
import pandas as pd
from tqdm import tqdm

def process(config):
    df = pd.read_pickle(config["preprocess"]["preprocessedPath"])
    df['created_at'] = df["created_at"].astype(str)
    ent = entityModel(config["process"]["entityModel"])
    sent = sentimentModel(config["process"]["sentimentModel"])

    with es(**config["elastic"]) as conn:
        print(conn.client.info())
        if not conn.client.indices.exists(config["process"]["indexName"]):
            conn.createIndex(config["process"]["indexName"])

        for index, row in tqdm(df.iterrows()):
            doc = {"text": row["trans"],
                   "user": int(row["author_id"]),
                   "timestamp": row["created_at"].split(" ")[0],
                   }
            for col in config["preprocess"]["columns"]:
                doc[col] = row[col]
            doc = {**doc, **ent.apply_pipeline(row["trans"]).format()}
            doc = {**doc, **sent.apply_pipeline(row["trans"]).format()}
            try:
                conn.write(config["process"]["indexName"], index, doc)
            except:
                print(doc)
                break




