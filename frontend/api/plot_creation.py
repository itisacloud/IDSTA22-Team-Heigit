import json
import random
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.express as px
from random import randrange

import datetime

import numpy as np
import plotly.io as pio

traces = []
df = pd.read_json('example.json')
def sort_entities(row):
    for outer_key in row:
        for inner_key in row[1]:
            print(inner_key)
            if inner_key == "n":
                return row[1][inner_key]


def square(row):

    sorted_dict =  sorted(row.items(), key=sort_entities, reverse=True)
    cnt = 0
    top_entities = []
    for tup in sorted_dict:
        if cnt < 5:
            top_entities.append(tup[0])
            cnt += 1
    return top_entities

df["top_entities"] = df["entities"].apply(square)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces

fig.add_trace(
    go.Bar(x=df["timestamps"],y=df["counts"], name="yaxis2 data", hoverinfo='skip',
           marker={'color': '#FFD700'}),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=df["timestamps"],
        y=df["sentiment"],
        customdata=np.stack((df['top_entities'], df['counts']), axis=-1),
        hovertemplate='<br>'.join([
            'Sentiment: %{y}',
            'Tweet Count: %{customdata[1]}',
            'Entitites : %{customdata[0]}',
        ]),
        line={'color': '#0057B8', "width": 5}),
    secondary_y=True,
)

#fig['layout']['yaxis']['autorange'] = "reversed"

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

#fig.write_html("test.html")
# plot_json = pio.to_json(fig)
# parsed=json.loads(plot_json)
# with open('test.json', 'w') as f:
#     json.dump(parsed, f)