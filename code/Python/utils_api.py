import pandas as pd
from pandas import DataFrame
from connections import elasticSearchConnection as es
from elasticsearch.helpers import scan



def getDocumentsById(conn:es, layer, id,index="tweets",timerange="2022-01-01:2023-01-01") -> list[dict]:
    query = {
        "query": {
            "bool": {
                "should": [
                ]
                , "filter": [
                    {"range": {"timestamp": {"gte": timerange.split(":")[0], "lte": timerange.split(":")[1]}}}]

            }}, "sort": [
            {"timestamp": "asc"}
        ]
    }
    es_response = scan(
        conn.client,
        index='tweets',
        query=query
    )
    docs = []
    for item in es_response:
        docs.append(item["_source"])
    return docs

def dataframeFromDocuments(documnets: list[dict]) -> DataFrame:
    df = pd.DataFrame.from_dict(documnets)

    df["date"] = pd.to_datetime(df.timestamp)
    return df
def groubByInterval(df: DataFrame, interval: str):
    if interval == "daily":  #
        return df.groupby(df.date.dt.day)
    elif interval == "weekly":
        return df.groupby(df.date.dt.week)
    elif interval == "monthly":
        return df.groupby(df.date.dt.month)

def createSentimentAvg(df, interval) -> list[float]:
    return groubByInterval(df, interval)['sentiment_score'].mean().tolist()

def getEntityDict(x,sent):
    import statistics
    d = {}
    sent = sent.tolist()
    x.tolist()
    print(len(x))
    print(len(sent))
    for i,ents  in enumerate(x):
        for ent in ents:
            print(ent)
            print(sent[i])
            try:
                d2 = d[f"{ent['word']}|{ent['type']}"]
                d2["n"]+=1
                d2["sentiments"]+= [sent[i]]
                d[f"{ent['word']}|{ent['type']}"] = d2
            except Exception:
                d2 = {}
                d2["n"]=1
                d2["sentiments"]= [sent[i]]
                d[f"{ent['word']}|{ent['type']}"] = d2
                pass
    for key, value in d.items():
        try:
            value["sentiment_sd"]=statistics.stdev(value["sentiments"])
        except:
            value["sentiment_sd"]="None"
            pass
        value["sentiment_mean"]=statistics.mean(value["sentiments"])
        d[key]=value
    return d

def createEntityCount(df, interval) -> list[dict]:
    return groubByInterval(df, interval).apply(lambda x:getEntityDict(x.enities,x.sentiment_score))

def createTweetCount(df, interval) -> list[int]:
    return groubByInterval(df, interval).apply(lambda x: len(x))

