import argparse
from preprocess import preprocess
from process import process

def readConfig(fp:str)->dict:
    import yaml
    with open(fp, "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return config

parser = argparse.ArgumentParser()

parser.add_argument("command",
                    action="store",
                    nargs='1',
                    default=None,
                    required=True,
                    choices=["preprocess","process","full"],)
parser.add_argument("-c","--config",
                    action="store",
                    nargs='1',
                    default=None,
                    required=True,
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

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from connections import elasticSearchConnection as es
import utils_api


app = FastAPI()
class Item(BaseModel):
    name: list[str]
    layer: list[str]
    interval: str
    timerange: Optional[str]
@app.post("/plot")
async def getPlots(item:Item):
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
        return response






