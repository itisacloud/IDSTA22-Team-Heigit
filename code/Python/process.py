from entityRecognition import entityModel
from sentiment import sentimentModel
from connections import elasticSearchConnection as es
import pandas as pd


def process(fp:str,host:str,cols,index:str="tweets"):
    df = pd.read_file(fp)
    ent = entityModel()
    sent = sentimentModel()
    con = es()
    for index, row in df.iterrows():
        doc = {"text":row["text"],
         "user":row["author_id"],
         "timestamp":row["created_at"],
        }
        for col in cols:
            doc[col]=row[col]
        doc+=ent.apply_pipeline(row["text"]).format()
        doc+=sent.apply_pipeline(row["text"]).format()
        es.write(index,index,doc)
