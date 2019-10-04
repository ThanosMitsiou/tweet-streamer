from src.tweet_streamer import TweetListener
from argparse import ArgumentParser

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



parser = ArgumentParser()
parser.add_argument('-t', '--track', type=str, nargs='+', dest='list',
                    help='List of items to listen to on tweets')

track_list = parser.parse_args().list
listener = TweetListener(track=track_list, is_async=True)

trace1 = go.Bar(name='values',
                x=list(listener.counts.keys()),
                y=list(listener.counts.values()))

app.layout = html.Div(
    html.Div([
        html.H4('Twitter Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph',
                  figure={'data': [trace1]}),
        dcc.Interval(
            id='interval-component',
            interval=3*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    top_hashtags = list(listener.counts.items())
    top_hashtags = sorted(top_hashtags, key=lambda x: x[1], reverse=True)[:10]

    return {'data': [go.Bar(x=[t[0] for t in top_hashtags],
                            y=[t[1] for t in top_hashtags])]}


if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
