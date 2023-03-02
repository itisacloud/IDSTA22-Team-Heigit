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
        timestamps = count.index.tolist()

        response = {

            "timestamps": timestamps,
            "sentiment": sentiment,
            "counts": count.tolist(),
            "entities": entities.tolist(),}
        return response







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

        fig.show()







