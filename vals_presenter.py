from dash import Dash, dcc, html
import plotly.express as px
import psycopg2
from vals_generator import PG_CONF
import pandas as pd


SELECT_VALUES_QUERY='''select ticker_value,processed_dttm from tickers_values where ticker_name=%s;
'''


def generate_graph(ticker_name):
    with psycopg2.connect(**PG_CONF) as conn:
        cur = conn.cursor()
        cur.execute(SELECT_VALUES_QUERY, (ticker_name,))
        res = cur.fetchall()
    # return res
    df = pd.DataFrame({
        "Time": [t for (_,t) in res],
        "Value": [v for (v,_) in res]
    })
    fig = px.line(df, x='Time', y='Value')    
    return fig



def generate_app():
    app = Dash(__name__)
    tick = 'ticker_03'
    fig = generate_graph(tick)
    tickers = [f'ticker_{i:02}' for i in range(99)]
    app.layout = html.Div(children=[
        html.H1('Showing_graphs'),
        html.Label('Chose a ticker'),

        dcc.Dropdown(tickers),
        dcc.Graph(id=tick,figure=generate_graph(tick)),
    ])
    return app

if __name__ == '__main__':
    app = generate_app()
    app.run_server(debug=True)
    # print(generate_graph('a'))