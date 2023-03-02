from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from main import readConfig
from connections import elasticSearchConnection as es
import utils_api

app = FastAPI()

class Item(BaseModel):
    name: list[str]
    layer: list[str]
    interval: str
    timerange: Optional[str]


config = readConfig("../default.config")



@app.post("/plot")
async def getPlots(item:Item):
    with es(**config["elastic"]) as conn:
        docs = utils_api.getDocumentsById(conn,item.layer,item.name,index="tweets") #add optional timerage
        df = utils_api.dataframeFromDocuments(docs)
        sentiment = utils_api.createSentimentAvg(df,item.interval)
        entities = utils_api.createEntityCount(df,item.interval)
        count = utils_api.createTweetCount(df,item.interval)
        response = {
            "timestamps": ["todo"],
            "sentiment" :sentiment.tolist(),
            "counts" : count.tolist(),
            "entities" : entities.tolist(),
        }






