import collections

import pandas as pd
from pandas import DataFrame
from connections import elasticSearchConnection as es
from elasticsearch.helpers import scan


def getDocumentsById(conn: es, layer: [str], id:[int], index: str = "tweets", timerange="2022-01-01:2023-01-01") -> list[dict]:
    query = {
        "query": {
            "bool": {
                "must": [
                ]
                , "filter": [
                    {"range": {"timestamp": {"gte": timerange.split(":")[0], "lte": timerange.split(":")[1]}}}]
            }}, "sort": [
            {"timestamp": "asc"}
        ]
    }
    for l,i in zip(layer,id):
        query["query"]["bool"]["must"].append({"match":{l:i}})
    print(query)

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


def listToShare(l):
    print(l)

    print(l)
    counter = collections.Counter(l)
    return [counter["positive"]/len(l),counter["negative"]/len(l)]

def createSentimentAvg(df, interval) -> list[float]:
    df["sentiment_label"] = df.apply(lambda x: [x.sentiment_label],axis=1)
    df_grouped = pd.DataFrame(groubByInterval(df, interval)["sentiment_label"].sum(),)
    #display(df_grouped)
    return df_grouped.apply(lambda x:listToShare(x.sentiment_label),axis=1).tolist()


def getEntityDict(x, sent):
    import statistics
    d = {}
    sent = sent.tolist()
    x.tolist()
    for i, ents in enumerate(x):
        for ent in ents:
            print(ent)
            print(sent[i])
            try:
                d2 = d[f"{ent['word']}|{ent['type']}"]
                d2["n"] += 1
                d2["sentiments"] += [sent[i]]
                d[f"{ent['word']}|{ent['type']}"] = d2
            except Exception:
                d2 = {}
                d2["n"] = 1
                d2["sentiments"] = [sent[i]]
                d[f"{ent['word']}|{ent['type']}"] = d2
                pass
    for key, value in d.items():
        try:
            value["sentiment_sd"] = statistics.stdev(value["sentiments"])
        except:
            value["sentiment_sd"] = "None"
            pass
        value["sentiment_mean"] = statistics.mean(value["sentiments"])
        d[key] = value
    return d


def createEntityCount(df: DataFrame, interval: str) -> DataFrame:
    return groubByInterval(df, interval).apply(lambda x: getEntityDict(x.enities, x.sentiment_score))


def createTweetCount(df: DataFrame, interval: str) -> DataFrame:
    return groubByInterval(df, interval).apply(lambda x: len(x))
