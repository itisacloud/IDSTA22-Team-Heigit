from entityRecognition import entityModel
from sentiment import sentimentModel
from connections import elasticSearchConnection as es
from main import readConfig

from os.path import join
import pandas as pd
from tqdm import tqdm


def createIndex(conn: es, name: str):
    mappings = {
        "properties": {
            "text": {"type": "text"},
            "user": {"type": "unsigned_long"},
            "timestamp": {"type": "date"},
            "NAME_0": {"type": "keyword"},
            "NAME_1": {"type": "keyword"},
            "NAME_2": {"type": "keyword"},
            "NAME_3": {"type": "keyword"},
            "enities": {
                "properties": {
                    "word": {"type": "keyword"},
                    "type": {"type": "keyword"}
                }
            },
            "sentiment": {
                "properties": {
                    "sentiment_label": {"type": "keyword"},
                    "sentiment_value": {"type": "float"}
                }
            }
        }
    }

    print(type(conn.client))
    conn.client.indices.create(index=name, mappings=mappings)



def process(config):
    df = pd.read_pickle(config["preprocess"]["preprocessedPath"])
    df['created_at'] = df["created_at"].astype(str)
    ent = entityModel(config["process"]["entityModel"])
    sent = sentimentModel(config["process"]["sentimentModel"])

    with es(**config["elastic"]) as conn:
        #conn.client.indices.delete(config["process"]["indexName"])
        print(conn.client.info())
        if not conn.client.indices.exists(config["process"]["indexName"]):
            createIndex(conn, config["process"]["indexName"])

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


if __name__ == "__main__":
    config = readConfig(join("..", "default.config"))
    process(config)
