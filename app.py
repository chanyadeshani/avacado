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

# import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

# Define the API endpoint URL
url = 'https://nss-container-p57byuk3wa-uc.a.run.app/api/ask'
url_categories = "https://nss-container-p57byuk3wa-uc.a.run.app/api/categories"
df = pd.DataFrame()  # Initialize an empty DataFrame


def make_api_request(query, noReviews,school_dropdown_value,course_group_dropdown_value, subject_dropdown_value):
    payload = {
        'school':school_dropdown_value,
        'course_group':course_group_dropdown_value,
        'subject':subject_dropdown_value,
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

def get_categories():
    response = requests.get(url_categories)

    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()

        # Return the processed data
        return data

categories = get_categories()

@app.callback(
    [
        dash.dependencies.Output('graph', 'figure'),
        dash.dependencies.Output('table1', 'data'),
        dash.dependencies.Output('table1', 'columns'),
        dash.dependencies.Output('table2', 'data'),
        dash.dependencies.Output('table2', 'columns'),
        dash.dependencies.Output('submit-button', 'disabled'),
        dash.dependencies.Output('table1_title', 'hidden'),
        dash.dependencies.Output('table2_title', 'hidden')

    ],
    [
        dash.dependencies.Input('submit-button', 'n_clicks'),
        dash.dependencies.Input('questions_dropdown', 'value'),
        
        dash.dependencies.Input('school_dropdown', 'value'),
        dash.dependencies.Input('course_group_dropdown', 'value'),
        dash.dependencies.Input('subject_dropdown', 'value'),
    ],
    [
        dash.dependencies.State('slider1', 'value'),
        dash.dependencies.State('passcode', 'value')

    ]
)

def handle_button_click(n_clicks, questions_dropdown_value, school_dropdown_value,course_group_dropdown_value, subject_dropdown_value, slider_value, passcode_value):
    ctx = dash.callback_context
    #print('check')
    if ctx.triggered:
        prop_id = ctx.triggered[0]['prop_id']

        if 'submit-button' in prop_id:
            print("Submit", school_dropdown_value,course_group_dropdown_value, subject_dropdown_value)
            if n_clicks is not None and n_clicks > 0 and questions_dropdown_value and passcode_value == 'nss23@UOG':
                # Call the make_api_request function with the input value
                print('api' ,questions_dropdown_value, slider_value,school_dropdown_value,course_group_dropdown_value, subject_dropdown_value)
                api_response = make_api_request(
                    questions_dropdown_value, slider_value,school_dropdown_value,course_group_dropdown_value, subject_dropdown_value)

                print(api_response)
                if api_response is not None :
                    # Extract the first child of the JSON object
                    reviews_data = api_response.get('reviews', [])

                    # Convert the first child to a DataFrame
                    df = pd.DataFrame(reviews_data)
                    if df.size > 0:
                    # Create a new column 'Review_trimmed' with trimmed text if length is greater than 100, else use the original text
                        df['Review_trimmed'] = df['Review'].apply(
                            lambda x: x[:120] + '...' if len(x) > 120 else x)
                        df_oct = pd.DataFrame(
                            columns=['Quadrants', 'Percentage'], index=range(5))
                        # Separate V-A scores to Quadrants
                        percentage_ph = len(df[(df['valence_score'] > 0) & (
                                df['arousal_score'] >= 0)]) / len(df)
                        df_oct.loc[0] = ['Awesome \n(Positive feeling with High intensity)', str(
                            round(percentage_ph * 100)) + '%']

                        percentage_pl = len(
                            df[(df['valence_score'] > 0) & (df['arousal_score'] < 0)]) / len(df)
                        df_oct.loc[1] = ['Okay \n(Positive feeling with Low intensity)', str(
                            round(percentage_pl * 100)) + '%']

                        percentage_nl = len(
                            df[(df['valence_score'] < 0) & (df['arousal_score'] < 0)]) / len(df)
                        df_oct.loc[2] = ['Unsatisfactory \n(Negative feeling with Low intensity)', str(
                            round(percentage_nl * 100)) + '%']

                        percentage_nh = len(
                            df[(df['valence_score'] < 0) & (df['arousal_score'] > 0)]) / len(df)
                        df_oct.loc[3] = ['Terrible \n (Negative feeling with High intensity)', str(
                            round(percentage_nh * 100)) + '%']
                        percentage_nh = len(
                            df[(df['valence_score'] == 0)]) / len(df)
                        df_oct.loc[4] = ['Neutral', str(
                            round(percentage_nh * 100)) + '%']

                        return (
                            {
                                'data': [
                                    {
                                        'x': df['valence_score'],
                                        'y': df['arousal_score'],
                                        'mode': 'markers',
                                        'hovertext': df['Review_trimmed'],
                                        'hoverinfo': df['Review_trimmed'],
                                    },
                                ],
                                'layout': {
                                    'title': 'Feeling and Intensity',
                                    'width': 800,  # Set the width of the figure
                                    'height': 500,  # Set the height of the figure
                                    'xaxis': {
                                        'title': '<────── Feeling ──────> ',
                                        'showticklabels': False,
                                        'color':'grey'
                                    },
                                    'yaxis': {
                                        'title': '<────── Intensity  ──────> ',
                                        'showticklabels': False,
                                        'color':'grey'
                                    },
                                    'annotations': [
                                        {
                                            'x': -1,  # X-coordinate of the annotation
                                            'y': 1,  # Y-coordinate of the annotation
                                            'text': 'Terrible',  # Text to display as the label
                                            'showarrow': False,  # Hide the arrow
                                            'font': {
                                                'color': 'red',  # Color of the text
                                                'size': 16  # Size of the text
                                            }
                                        },
                                        {
                                            'x': -1,  # X-coordinate of the annotation
                                            'y': -1,  # Y-coordinate of the annotation
                                            'text': 'Unsatisfactory',  # Text to display as the label
                                            'showarrow': False,  # Hide the arrow
                                            'font': {
                                                'color': 'black',  # Color of the text
                                                'size': 16  # Size of the text
                                            }
                                        },
                                        {
                                            'x': 1,  # X-coordinate of the annotation
                                            'y': -1,  # Y-coordinate of the annotation
                                            'text': 'Okay',  # Text to display as the label
                                            'showarrow': False,  # Hide the arrow
                                            'font': {
                                                'color': 'blue',  # Color of the text
                                                'size': 16  # Size of the text
                                            }
                                        },
                                        {
                                            'x': 1,  # X-coordinate of the annotation
                                            'y': 1,  # Y-coordinate of the annotation
                                            'text': 'Awesome',  # Text to display as the label
                                            'showarrow': False,  # Hide the arrow
                                            'font': {
                                                'color': 'green',  # Color of the text
                                                'size': 16  # Size of the text
                                            }
                                        },
                                    ]
                                }
                            },
                            df_oct.to_dict('records'),
                            [{"name": col, "id": col}
                            for col in df_oct.columns[:2]],
                            df.to_dict('records'),
                            [{"name": col, "id": col} for col in df.columns[:2]],
                            False,  # Enable the submit button
                            False,
                            False
                        )
                else:
                    return blank_fig(), [], [], [], [], True, True, True  # Disable the submit button

    # Disable the submit button if the input value is empty
    return blank_fig(), [], [], [], [], not bool(questions_dropdown_value), True, True


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

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
            style={'display': 'grid', 'grid-template-columns': '1fr 10fr', 'margin-left': '50px'},
            children=[
                html.H4(
                    children='Passcode',
                    style={}
                ),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Input(
                            id='passcode',
                            type='password',
                            placeholder='Passcode Here',
                            style={'display': 'block', 'width': '100%', 'max-width': '290px', 'height': '30px',
                                   'align-items': 'center'}
                        )]
                ),
                html.H4(children='Institute',
                        style={}),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Dropdown(
                            options=[{'label': x, 'value': x}
                                     for x in sorted(
                                    ['University of Aberdeen', 'Abertay University', 'Aberystwyth University',
                                     'Anglia Ruskin University', 'Arden University',
                                     'Aston University, Birmingham', 'Bangor University', 'University of Bath',
                                     'Bath Spa University', 'University of Bedfordshire',
                                     'BIMM University', 'University of Birmingham', 'Birmingham City University',
                                     'University College Birmingham', 'Bishop Grosseteste University, Lincoln',
                                     'University of Bolton', 'The Arts University Bournemouth',
                                     'Bournemouth University', 'BPP University', 'University of Bradford',
                                     'University of Brighton',
                                     'University of Bristol', 'Brunel University', 'University of Buckingham',
                                     'Buckinghamshire New University', 'University of Cambridge',
                                     'Canterbury Christ Church University', 'Cardiff Metropolitan University',
                                     'Cardiff University', 'University of Chester',
                                     'University of Chichester', 'Coventry University', 'Cranfield University',
                                     'University for the Creative Arts', 'University of Cumbria',
                                     'De Montfort University', 'University of Derby', 'University of Dundee',
                                     'Durham University', 'University of East Anglia', 'University of East London',
                                     'Edge Hill University', 'University of Edinburgh', 'Edinburgh Napier University',
                                     'University of Essex', 'University of Exeter', 'Falmouth University',
                                     'University of Glasgow',
                                     'Glasgow Caledonian University', 'University of Gloucestershire',
                                     'University of Greenwich', 'Harper Adams University', 'Hartpury University',
                                     'Heriot-Watt University', 'University of Hertfordshire',
                                     'University of the Highlands & Islands', 'University of Huddersfield',
                                     'University of Hull',
                                     'Imperial College London', 'Keele University', 'University of Kent',
                                     'Kingston University', 'University of Central Lancashire', 'Lancaster University',
                                     'University of Leeds', 'Leeds Arts University', 'Leeds Beckett University',
                                     'Leeds Trinity University', 'University of Leicester', 'University of Lincoln',
                                     'University of Liverpool', 'Liverpool Hope University',
                                     'Liverpool John Moores University', 'University of London',
                                     'London Metropolitan University',
                                     'London School of Economics', 'London South Bank University',
                                     'Loughborough University', 'University of Manchester',
                                     'Manchester Metropolitan University',
                                     'Middlesex University', 'Newcastle University', 'Newman University',
                                     'University of Northampton', 'Northeastern University-London',
                                     'Northumbria University',
                                     'Norwich University of the Arts', 'University of Nottingham',
                                     'Nottingham Trent University', 'The Open University', 'University of Oxford',
                                     'Oxford Brookes University',
                                     'Plymouth Marjon University', 'Arts University Plymouth', 'University of Plymouth',
                                     'University of Portsmouth', 'Queen Margaret University',
                                     "Queen's University Belfast", 'Ravensbourne University London',
                                     'University of Reading', "Regent's University London",
                                     'Richmond American University London',
                                     'The Robert Gordon University', 'Roehampton University',
                                     'Royal Agricultural University', 'Royal Holloway, University of London',
                                     'University of Salford', 'University of Sheffield',
                                     'Sheffield Hallam University', 'University of South Wales',
                                     'University of Southampton', 'Solent University', 'University of St Andrews',
                                     "St George's, University of London",
                                     "St Mary's University, Twickenham", 'Staffordshire University',
                                     'University of Stirling', 'University of Strathclyde', 'University of Suffolk',
                                     'University of Sunderland', 'University of Surrey', 'University of Sussex',
                                     'Swansea University', 'Teesside University', 'University of the Arts London',
                                     'Ulster University', 'University of Law', 'University of Wales',
                                     'University of Wales', 'University of Warwick',
                                     'University of the West of England',
                                     'University of the West of Scotland', 'University of West London',
                                     'University of Westminster', 'University of Winchester',
                                     'University of Wolverhampton',
                                     'University of Worcester', 'Wrexham Glyndŵr University', 'University of York',
                                     'York St John University']
                                )],
                            value='University of Gloucestershire',
                            id='university_dropdown',
                            style={'width': '100%', 'max-width': '300px', 'display': 'block'}
                        )]
                ),
                html.H4(children='School',
                        style={}),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Dropdown(
                            # options=['School of arts', 'Gloucestershire business school',
                            #          'School of computing and engineering',
                            #          'School of creative industries', 'School of education and humanities',
                            #          'School of health and social care', 'School of natural, social and sport science',
                            #          'Countryside and community research institute'],
                            options=categories['school'],
                            value=categories['school'][0],
                            id='school_dropdown',
                            style={'width': '100%', 'max-width': '300px', 'display': 'block'}
                        )]
                ),
                html.H4(children='Subject',
                        style={'justifyContent': 'center', 'alignItems': 'center'}),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Dropdown(
                            # options=['Subject 1', 'Subject 2', 'Subject 3'],
                            options=categories['subject'],
                            value=categories['subject'][0],
                            id='subject_dropdown',
                            style={'width': '100%', 'max-width': '300px', 'display': 'block'}
                        )]
                ),
                html.H4(children='Course Group',
                        style={'justifyContent': 'center', 'alignItems': 'center'}),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Dropdown(
                            # options=['Subject 1', 'Subject 2', 'Subject 3'],
                            options=categories['course_group'],
                            value=categories['course_group'][0],
                            id='course_group_dropdown',
                            style={'width': '100%', 'max-width': '300px', 'display': 'block'}
                        )]
                ),
                html.H4(
                    children='Category',
                    style={}
                ),
                html.Div(
                    style={'display': 'flex', 'align-items': 'center'},
                    children=[
                        dcc.Dropdown(
                            options=['Teaching on my course', 'Learning opportunities', 'Assessment and feedback',
                                     'Academic support',
                                     'Organisation and management', 'Learning resources', 'Student Voice'],
                            value='Teaching on my course',
                            id='questions_dropdown',
                            style={'width': '100%', 'max-width': '300px', 'display': 'block'}
                        )]
                ),
                html.H4(children='No of Reviews ',
                        style={'justifyContent': 'center',
                               'alignItems': 'center', 'marginTop': '35px'}
                        ),

                html.Div(
                    style={'marginTop': '30px', 'height': '30px', 'align-items': 'center', 'display': 'flex'},
                    children=[
                        daq.Slider(
                            id='slider1',
                            min=0,
                            max=300,
                            value=50,
                            handleLabel={"showCurrentValue": True,
                                         "label": " ", "style": {"fontSize": 30}},
                            step=10,
                            color="#888888"
                        ),
                    ]
                ),
                html.Div(
                    style={'width': '100%', 'alignItems': 'center'},
                    children=[
                        html.Button('Submit', id='submit-button', n_clicks=0,
                                        style={
                                        'display': 'inline-flex',
                                        'align-items': 'center',
                                        'width': '100px',
                                        'height': '40px',
                                        'font-size': '18px',
                                        'border': 'none',
                                        'border-radius': '4px',
                                        'background-color': '#007bff',
                                        'color': '#ffffff',
                                        'cursor': 'pointer',
                                        'padding': '8px 20px',
                                        'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)',
                                    },
                                    disabled=True)]),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'align-items': 'center',
                   'justify-content': 'center'},
            children=[
                dcc.Graph(id='graph', figure=blank_fig(), style={
                    'width': '800px', 'height': '500px'})
            ]
        ),
        html.H3(children='Percentage of reviews in each quadrant',
                hidden=True, id='table1_title',style={'margin-left': '30px'}),
        dash_table.DataTable(
            id='table1',
            columns=[],
            data=[],
            style_table={'width': '40%',
                         'marginLeft': '30px', 'marginRight': '30px'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'text-align': 'left'
            },
        ),
        html.H3(children="Reviews and it's similarity to the category selected",
                hidden=True, id='table2_title',style={'margin-left': '30px'}),
        dash_table.DataTable(
            id='table2',
            columns=[],
            data=[],
            style_table={'width': '95%',
                         'marginLeft': '30px', 'marginRight': '30px'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'width': 'auto',
                'text-align': 'left'
            },
        ),
    ]
)

if __name__ == '__main__':
    PORT = os.getenv('PORT', 8050)
    app.run_server(debug=True, port=PORT, host='0.0.0.0')
