from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import pandas as pd
from .models import Ticker, TickerValue


def initiate_tickerboard(server):
    app = Dash(server=server, routes_pathname_prefix='/tickerboard/')
    res=Ticker.query.all()
    tickers = [t.tickername for t in res]
    app.layout = html.Div(children=[
        html.H1('Showing_graphs'),
        html.Label('Chose a ticker'),

        dcc.Dropdown(
            tickers,
            'choose_ticker',
            id='choose_ticker'
        ),
        dcc.Graph(
            id='ticker_graph'
        ),
        dcc.Interval(
            id='interval_component',
            interval=1*1000,
            n_intervals=0
        )
    ])
    return app.server


@callback(Output('ticker_graph', 'figure'), [Input('choose_ticker', 'value'), Input('interval_component', 'n_intervals')])
def update_graph(ticker,n):
    ticker_id = Ticker.query.filter(Ticker.tickername == ticker).first().id
    res = TickerValue\
        .query\
        .filter(TickerValue.ticker_id == ticker_id)\
        .order_by(TickerValue.processed_dttm)\
        .all()
    df = pd.DataFrame({
        "Time": [t.processed_dttm for t in res],
        "Value": [t.ticker_value for t in res]
    })
    fig = px.line(df, x='Time', y='Value')    
    return fig
