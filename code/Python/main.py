import argparse
from preprocess import preprocess
from process import process

def readConfig(fp:str)->dict:
    import yaml
    with open(fp, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("command",
                        action="store",
                        default=None,
                        choices=["preprocess","process","full","full+bulk","api","bulk"],)

    parser.add_argument("-c","--config",
                        action="store",
                        default="default.config",
                        required=True
                        )

    args = parser.parse_args()

    config = readConfig(args.config)

    if args.command == "preprocess":
        preprocess(config)
    if args.command == "process":
        process(config)

    if args.command == "api":
        import uvicorn
        uvicorn.run("main:app")


    if args.command == "bulk":
        from connections import elasticSearchConnection as es
        with es(**config["elastic"]) as conn:
            conn.bulkImport(config["process"]["indexName"],config["bulk"]["filepath"])

    if args.command == "full":
        preprocess(config)
        process(config)
        import uvicorn
        uvicorn.run("main:app")

    if args.command == "full+bulk":
        from connections import elasticSearchConnection as es
        with es(**config["elastic"]) as conn:
            conn.bulkImport(config["process"]["indexName"], config["bulk"]["filepath"])
        import uvicorn
        uvicorn.run("main:app")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from connections import elasticSearchConnection as es
import utils_api

config = readConfig("../default.config")

app = FastAPI()
class Item(BaseModel):
    name: list[str]
    layer: list[str]
    interval: str
    timerange: Optional[str]
@app.post("/plot")
async def getPlots(item:Item):
    import pandas as pd
    from plotly.offline import plot
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    import plotly.express as px
    from random import randrange

    import datetime

    import numpy as np
    import plotly.io as pio

    with es(**config["elastic"]) as conn:
        docs = utils_api.getDocumentsById(conn,item.layer,item.name,index="tweets") #add optional timerage
    df = utils_api.dataframeFromDocuments(docs)
    sentiment = utils_api.createSentimentAvg(df,item.interval)
    entities = utils_api.createEntityCount(df,item.interval)
    count = utils_api.createTweetCount(df,item.interval)
    timestamps = count.index.tolist()

    response = {

        "timestamps": timestamps,
        "sentiment": sentiment,
        "counts": count.tolist(),
        "entities": entities.tolist()}

    """
    traces = []
    df = pd.DataFrame.fromdict(response)
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces

    fig.add_trace(
        go.Bar(y=df["counts"], name="yaxis2 data", hoverinfo='skip',
               marker={'color': '#FFD700'}),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            # x=df["timestamps"],
            y=df["sentiment"],
            customdata=np.stack((df['entities'], df['counts']), axis=-1),
            hovertemplate='<br>'.join([
                'Sentiment: $%{y}',
                'Tweet Count: %{customdata[1]}'
                'Entitites : %{customdata[0]}',
            ]),
            line={'color': '#0057B8', "width": 5}),
        secondary_y=False,
    )
    fig['layout']['yaxis']['autorange'] = "reversed"
    # Add figure title
    fig.update_layout(
        title_text="Twitter Sentiment Analysis",
        bargap=0.0,
        plot_bgcolor='rgb(207, 226, 243)'
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Date")
    # Set y-axes titles
    fig.update_yaxes(title_text="Sentiment", secondary_y=False)
    fig.update_yaxes(title_text="Tweet Count", secondary_y=True)
    fig.show()"""
    return response







