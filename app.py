import pandas as pd
import os
import numpy as np
import requests
import json
import dash
from dash import dash_table
from dash import dcc
from dash import html
import plotly.graph_objects as go

#import dash_bootstrap_components as dbc


app = dash.Dash(__name__)

# Define the API endpoint URL
url = 'https://nss-container-p57byuk3wa-uc.a.run.app/api/ask'
df = pd.DataFrame()  # Initialize an empty DataFrame

def make_api_request(query):
    payload = {
        'query': query,
        'top_n': 30,
        'threshold': 0.75
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Return the processed data
        return data

@app.callback(
    [dash.dependencies.Output('graph', 'figure'),
     dash.dependencies.Output('table1', 'data'),
     dash.dependencies.Output('table1', 'columns')],
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input1', 'value')]
)
def handle_button_click(n_clicks, input_value):
    if n_clicks is not None and n_clicks > 0:
        # Call the make_api_request function with the input value
        api_response = make_api_request(input_value)

        if api_response is not None:
            # Extract the first child of the JSON object
            reviews_data = api_response.get('reviews', [])

            # Convert the first child to a DataFrame
            df = pd.DataFrame(reviews_data)

            return (
                {
                    'data': [
                        {
                            'x': df['valence_score'],
                            'y': df['arousal_score'],
                            'mode': 'markers',
                            'hovertext': df['Review'],
                            'hoverinfo': df['Review'],
                        },
                    ],
                    'layout': {
                        'title': 'Valence and Arousal',
                        'width': 800,  # Set the width of the figure
                        'height': 500,  # Set the height of the figure
                    }
                },
                df.to_dict('records'),
                [{"name": col, "id": col} for col in df.columns[:2]]
            )
        else:
            return {}, [],[]
    else:
        return {}, [],[]
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig
app.layout = html.Div(
    children=[
        html.H1(children='National Student Survey'),
        html.H2(children='Analysis of student comments'),
        dcc.Input(id='input1', type='text', placeholder='Enter your question', style={'marginRight': '10px'}),
        html.Button('Submit', id='submit-button', n_clicks=0),
        dcc.Graph(id='graph',  figure = blank_fig()),
        dash_table.DataTable(
            id='table1',
            columns=[],  # Only display first two columns
            data=[],
            style_table={'width': '80%'},
            style_cell={
                'maxWidth': '50px',  # Limiting cell width to 20 characters
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
        ),
    ]
)


if __name__ == '__main__':
    PORT = os.getenv('PORT', 8050)
    app.run_server(debug=True, port=PORT, host='0.0.0.0')
