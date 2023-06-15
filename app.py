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
import dash_daq as daq


#import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

# Define the API endpoint URL
url = 'https://nss-container-p57byuk3wa-uc.a.run.app/api/ask'
df = pd.DataFrame()  # Initialize an empty DataFrame

def make_api_request(query, noReviews):
    payload = {
        'query': query,
        'top_n': noReviews,
        'threshold': 0.75
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Return the processed data
        return data


@app.callback(
    [
        dash.dependencies.Output('graph', 'figure'),
        dash.dependencies.Output('table1', 'data'),
        dash.dependencies.Output('table1', 'columns'),
        dash.dependencies.Output('submit-button', 'disabled')
    ],
    [
        dash.dependencies.Input('submit-button', 'n_clicks'),
        dash.dependencies.Input('input1', 'value')
    ],
    [
        dash.dependencies.State('slider1', 'value')
    ]
)
def handle_button_click(n_clicks, input_value, slider_value):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']

        if 'submit-button' in prop_id:
            if n_clicks is not None and n_clicks > 0 and input_value:
                # Call the make_api_request function with the input value
                api_response = make_api_request(input_value, slider_value)

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
                                'xaxis': {
                                    'title': 'Valence Score'
                                },
                                'yaxis': {
                                    'title': 'Arousal Score'
                                },
                                'annotations': [
                                    # Annotations code here
                                ]
                            }
                        },
                        df.to_dict('records'),
                        [{"name": col, "id": col} for col in df.columns[:2]],
                        False  # Enable the submit button
                    )
                else:
                    return blank_fig(), [], [], True  # Disable the submit button

    # Disable the submit button if the input value is empty
    return blank_fig(), [], [], not bool(input_value)

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig
app.layout = html.Div(
    children=[
        html.Div(
            style={'text-align': 'center', 'marginBottom': '40px'},
            children=[
                html.H1(children='National Student Survey'),
                html.H2(children='Analysis of student comments'),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin': '0 20px'},
            children=[
                dcc.Input(
                    id='input1',
                    type='text',
                    placeholder='Enter your question',
                    style={'marginRight': '10px', 'width': '500px', 'height': '30px'}
                ),
                daq.Slider(
                    id='slider1',
                    min=0,
                    max=300,
                    value=50,
                    handleLabel={"showCurrentValue": True, "label": "No of Reviews", "style": {"fontSize": 30}},
                    step=10,
                    color="#888888"
                ),
                html.Button('Submit', id='submit-button', n_clicks=0,
                            style={'marginLeft': '30px', 'width': '70px', 'height': '30px'}, disabled=True)
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'},
            children=[
                dcc.Graph(id='graph', figure=blank_fig(), style={'width': '800px', 'height': '500px'})
            ]
        ),
        dash_table.DataTable(
            id='table1',
            columns=[],  # Only display first two columns
            data=[],
            style_table={'width': '98%', 'marginLeft': '30px','marginRight': '30px'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'text-align': 'left'
            },            
        ),
    ]
)

if __name__ == '__main__':
    PORT = os.getenv('PORT', 8050)
    app.run_server(debug=True, port=PORT, host='0.0.0.0')
