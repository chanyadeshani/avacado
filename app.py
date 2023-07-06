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
url = "https://nss-container-p57byuk3wa-uc.a.run.app/api/ask"
url_categories = "https://nss-container-p57byuk3wa-uc.a.run.app/api/categories"
options =[]
course_options =[]

def make_api_request(query, noReviews,school_dropdown_value,course_group_dropdown_value, subject_dropdown_value):
    payload = {
        "school":school_dropdown_value,
        "course_group":course_group_dropdown_value,
        "subject":subject_dropdown_value,
        "query": query,
        "top_n": noReviews,
        "threshold": 0.75
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
structure = categories["structure"]

@app.callback(
    [
        dash.dependencies.Output("graph", "figure"),
        dash.dependencies.Output("table1", "data"),
        dash.dependencies.Output("table1", "columns"),
        dash.dependencies.Output("table_awesome", "data"),
        dash.dependencies.Output("table_awesome", "columns"),
        dash.dependencies.Output("table_ok", "data"),
        dash.dependencies.Output("table_ok", "columns"),
        dash.dependencies.Output("table_unsatis", "data"),
        dash.dependencies.Output("table_unsatis", "columns"),
        dash.dependencies.Output("table_terrible", "data"),
        dash.dependencies.Output("table_terrible", "columns"),
        dash.dependencies.Output("table_nutral", "data"),
        dash.dependencies.Output("table_nutral", "columns"),
        dash.dependencies.Output("submit-button", "disabled"),
        dash.dependencies.Output("table_awesome_title", "hidden"),
        dash.dependencies.Output("table_ok_title", "hidden"),
        dash.dependencies.Output("table_unsatis_title", "hidden"),
        dash.dependencies.Output("table_terrible_title", "hidden"),
        dash.dependencies.Output("table_nutral_title", "hidden")

    ],
    [
        dash.dependencies.Input("submit-button", "n_clicks"),
        dash.dependencies.Input("questions_dropdown", "value"),
        dash.dependencies.Input("school_dropdown", "value"),
        dash.dependencies.Input("course_group_dropdown", "value"),
        dash.dependencies.Input("subject_dropdown", "value"),
    ],
    [
        dash.dependencies.State("slider1", "value"),
        dash.dependencies.State("passcode", "value")
    ]
)

def handle_button_click(n_clicks, questions_dropdown_value, school_dropdown_value,course_group_dropdown_value, subject_dropdown_value, slider_value, passcode_value):
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"]

        if "submit-button" in prop_id:
            if n_clicks is not None and n_clicks > 0 and questions_dropdown_value and passcode_value == "nss23@UOG":
                # Call the make_api_request function with the input value
                api_response = make_api_request(
                    questions_dropdown_value, slider_value,school_dropdown_value,course_group_dropdown_value, subject_dropdown_value)

                if api_response is not None :
                    # Extract the first child of the JSON object
                    reviews_data = api_response.get("reviews", [])

                    # Convert the first child to a DataFrame
                    df = pd.DataFrame(reviews_data)
                    if df.size > 0:
                    # Create a new column "Review_trimmed" with trimmed text if length is greater than 100, else use the original text
                        df["Review_trimmed"] = df["Review"].apply(
                            lambda x: x[:120] + "..." if len(x) > 120 else x)
                        df_oct = pd.DataFrame(
                            columns=["Quadrants", "Percentage"], index=range(5))
                        # Separate V-A scores to Quadrants
                        percentage_ph = len(df[(df["valence_score"] > 0) & (
                                df["arousal_score"] >= 0)]) / len(df)
                        df_oct.loc[0] = ["Awesome \n(Positive feeling with High intensity)", str(
                            round(percentage_ph * 100)) + "%"]

                        percentage_pl = len(
                            df[(df["valence_score"] > 0) & (df["arousal_score"] < 0)]) / len(df)
                        df_oct.loc[1] = ["Okay \n(Positive feeling with Low intensity)", str(
                            round(percentage_pl * 100)) + "%"]

                        percentage_nl = len(
                            df[(df["valence_score"] < 0) & (df["arousal_score"] < 0)]) / len(df)
                        df_oct.loc[2] = ["Unsatisfactory \n(Negative feeling with Low intensity)", str(
                            round(percentage_nl * 100)) + "%"]

                        percentage_nh = len(
                            df[(df["valence_score"] < 0) & (df["arousal_score"] > 0)]) / len(df)
                        df_oct.loc[3] = ["Terrible \n (Negative feeling with High intensity)", str(
                            round(percentage_nh * 100)) + "%"]
                        percentage_nh = len(
                            df[(df["valence_score"] == 0)]) / len(df)
                        df_oct.loc[4] = ["Nothing stands out \n (Neutral feeling)", str(
                            round(percentage_nh * 100)) + "%"]
                        
                        df_pvhi = df[(df["valence_score"] > 0) & (df["arousal_score"] > 0)].sort_values(by=['arousal_score'], ascending=False)
                        df_pvli = df[(df["valence_score"] > 0) & (df["arousal_score"] < 0)].sort_values(by=['arousal_score'], ascending=False)
                        df_nvli = df[(df["valence_score"] < 0) & (df["arousal_score"] < 0)].sort_values(by=['arousal_score'], ascending=False)
                        df_nvhi = df[(df["valence_score"] < 0) & (df["arousal_score"] > 0)].sort_values(by=['arousal_score'], ascending=False)
                        df_nu = df[(df["valence_score"] == 0)].sort_values(by=['arousal_score'], ascending=False)
                    
                        return (
                            {
                                "data": [
                                    {
                                        "x": df["valence_score"],
                                        "y": df["arousal_score"],
                                        "mode": "markers",
                                        "hovertext": df["Review_trimmed"],
                                        "hoverinfo": df["Review_trimmed"],
                                    },
                                ],
                                "layout": {
                                    "title": "Feeling and Intensity",
                                    "width": 800,  # Set the width of the figure
                                    "height": 500,  # Set the height of the figure
                                    "xaxis": {
                                        "title": "<────── Feeling ──────> ",
                                        "showticklabels": False,
                                        "color":"grey"
                                    },
                                    "yaxis": {
                                        "title": "<────── Intensity  ──────> ",
                                        "showticklabels": False,
                                        "color":"grey"
                                    },
                                    "annotations": [
                                        {
                                            "x": -1,  # X-coordinate of the annotation
                                            "y": 1,  # Y-coordinate of the annotation
                                            "text": "Terrible",  # Text to display as the label
                                            "showarrow": False,  # Hide the arrow
                                            "font": {
                                                "color": "red",  # Color of the text
                                                "size": 16  # Size of the text
                                            }
                                        },
                                        {
                                            "x": -1,  # X-coordinate of the annotation
                                            "y": -1,  # Y-coordinate of the annotation
                                            "text": "Unsatisfactory",  # Text to display as the label
                                            "showarrow": False,  # Hide the arrow
                                            "font": {
                                                "color": "black",  # Color of the text
                                                "size": 16  # Size of the text
                                            }
                                        },
                                        {
                                            "x": 1,  # X-coordinate of the annotation
                                            "y": -1,  # Y-coordinate of the annotation
                                            "text": "Okay",  # Text to display as the label
                                            "showarrow": False,  # Hide the arrow
                                            "font": {
                                                "color": "blue",  # Color of the text
                                                "size": 16  # Size of the text
                                            }
                                        },
                                        {
                                            "x": 1,  # X-coordinate of the annotation
                                            "y": 1,  # Y-coordinate of the annotation
                                            "text": "Awesome",  # Text to display as the label
                                            "showarrow": False,  # Hide the arrow
                                            "font": {
                                                "color": "green",  # Color of the text
                                                "size": 16  # Size of the text
                                            }
                                        },
                                    ]
                                }
                            },
                            df_oct.to_dict("records"),# percentage tabel
                            [{"name": col, "id": col} for col in df_oct.columns[:2]],
                            df_pvhi.to_dict("records"), # awesome table
                            [{"name": col, "id": col} for col in df_pvhi.columns[:2]],
                            df_pvli.to_dict("records"), # ok table
                            [{"name": col, "id": col} for col in df_pvli.columns[:2]],
                            df_nvli.to_dict("records"), # unsatis table
                            [{"name": col, "id": col} for col in df_nvli.columns[:2]],
                            df_nvhi.to_dict("records"), # terrible table
                            [{"name": col, "id": col} for col in df_nvhi.columns[:2]],
                            df_nu.to_dict("records"), # nutral table
                            [{"name": col, "id": col} for col in df_nu.columns[:2]],
                            False,  # Enable the submit button
                            False, # Show table titles
                            False,
                            False,
                            False,
                            False
                        )
                else:
                    return blank_fig(), [], [], [], [], [], [], [], [], [], [], [], [], True, True, True, True, True,True  # Disable the submit button

    # Disable the submit button if the input value is empty
    return blank_fig(), [], [], [], [], [], [], [], [], [], [], [], [], not bool(questions_dropdown_value), True, True,True, True,True


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

@app.callback(
    dash.dependencies.Output('subject_dropdown', 'options'),
    [dash.dependencies.Input('school_dropdown', 'value')]
)
def update_subject_dropdown(selected_value):
    school_list = list(structure.keys())
    if selected_value in school_list:
        options = list(structure[selected_value].keys())
    
    else:
        options = [] 

    return options
       
@app.callback(
    dash.dependencies.Output('course_group_dropdown', 'options'),
     [dash.dependencies.Input('school_dropdown', 'value'),
        dash.dependencies.Input('subject_dropdown', 'value')]
)
def update_subject_dropdown(school,subject):
    course_options = []
    if school:
        course_list = list(structure[school].keys())
        if subject and subject in course_list:
            course_options = structure[school][subject]["course_group"]

    return course_options

app.layout = html.Div(
    children=[
        html.Div(
            style={"text-align": "center", "marginBottom": "40px"},
            children=[
                html.H1(children="National Student Survey"),
                html.H2(children="Analysis of student comments"),
            ]
        ),
        html.Div(
            style={"display": "grid", "grid-template-columns": "1fr 10fr", "margin-left": "50px"},
            children=[
                html.H4(
                    children="Passcode",
                    style={}
                ),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Input(
                            id="passcode",
                            type="password",
                            placeholder="Passcode Here",
                            style={"display": "block", "width": "100%", "max-width": "290px", "height": "30px",
                                   "align-items": "center"}
                        )]
                ),
                html.H4(children="Institute",
                        style={}),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            options=[{"label": x, "value": x}
                                     for x in sorted(
                                    ["University of Aberdeen", "Abertay University", "Aberystwyth University",
                                     "Anglia Ruskin University", "Arden University",
                                     "Aston University, Birmingham", "Bangor University", "University of Bath",
                                     "Bath Spa University", "University of Bedfordshire",
                                     "BIMM University", "University of Birmingham", "Birmingham City University",
                                     "University College Birmingham", "Bishop Grosseteste University, Lincoln",
                                     "University of Bolton", "The Arts University Bournemouth",
                                     "Bournemouth University", "BPP University", "University of Bradford",
                                     "University of Brighton",
                                     "University of Bristol", "Brunel University", "University of Buckingham",
                                     "Buckinghamshire New University", "University of Cambridge",
                                     "Canterbury Christ Church University", "Cardiff Metropolitan University",
                                     "Cardiff University", "University of Chester",
                                     "University of Chichester", "Coventry University", "Cranfield University",
                                     "University for the Creative Arts", "University of Cumbria",
                                     "De Montfort University", "University of Derby", "University of Dundee",
                                     "Durham University", "University of East Anglia", "University of East London",
                                     "Edge Hill University", "University of Edinburgh", "Edinburgh Napier University",
                                     "University of Essex", "University of Exeter", "Falmouth University",
                                     "University of Glasgow",
                                     "Glasgow Caledonian University", "University of Gloucestershire",
                                     "University of Greenwich", "Harper Adams University", "Hartpury University",
                                     "Heriot-Watt University", "University of Hertfordshire",
                                     "University of the Highlands & Islands", "University of Huddersfield",
                                     "University of Hull",
                                     "Imperial College London", "Keele University", "University of Kent",
                                     "Kingston University", "University of Central Lancashire", "Lancaster University",
                                     "University of Leeds", "Leeds Arts University", "Leeds Beckett University",
                                     "Leeds Trinity University", "University of Leicester", "University of Lincoln",
                                     "University of Liverpool", "Liverpool Hope University",
                                     "Liverpool John Moores University", "University of London",
                                     "London Metropolitan University",
                                     "London School of Economics", "London South Bank University",
                                     "Loughborough University", "University of Manchester",
                                     "Manchester Metropolitan University",
                                     "Middlesex University", "Newcastle University", "Newman University",
                                     "University of Northampton", "Northeastern University-London",
                                     "Northumbria University",
                                     "Norwich University of the Arts", "University of Nottingham",
                                     "Nottingham Trent University", "The Open University", "University of Oxford",
                                     "Oxford Brookes University",
                                     "Plymouth Marjon University", "Arts University Plymouth", "University of Plymouth",
                                     "University of Portsmouth", "Queen Margaret University",
                                     "Queen's University Belfast", "Ravensbourne University London",
                                     "University of Reading", "Regent's University London",
                                     "Richmond American University London",
                                     "The Robert Gordon University", "Roehampton University",
                                     "Royal Agricultural University", "Royal Holloway, University of London",
                                     "University of Salford", "University of Sheffield",
                                     "Sheffield Hallam University", "University of South Wales",
                                     "University of Southampton", "Solent University", "University of St Andrews",
                                     "St George's, University of London",
                                     "St Mary's University, Twickenham", "Staffordshire University",
                                     "University of Stirling", "University of Strathclyde", "University of Suffolk",
                                     "University of Sunderland", "University of Surrey", "University of Sussex",
                                     "Swansea University", "Teesside University", "University of the Arts London",
                                     "Ulster University", "University of Law", "University of Wales",
                                     "University of Wales", "University of Warwick",
                                     "University of the West of England",
                                     "University of the West of Scotland", "University of West London",
                                     "University of Westminster", "University of Winchester",
                                     "University of Wolverhampton",
                                     "University of Worcester", "Wrexham Glyndŵr University", "University of York",
                                     "York St John University"]
                                )],
                            value="University of Gloucestershire",
                            id="university_dropdown",
                            style={"width": "100%", "max-width": "300px", "display": "block"}
                        )]
                ),
                html.H4(children="School",
                        style={}),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            options=[{"label": x, "value": x} for x in sorted(structure.keys())],
                            id="school_dropdown",
                            style={"width": "100%", "max-width": "300px", "display": "block"}
                        )]
                ),
                html.H4(children="Subject",
                        style={"justifyContent": "center", "alignItems": "center"}),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            options=options,
                            value=options[0]['value'] if options else None,
                            #placeholder = "Select a School First",
                            id="subject_dropdown",
                            style={"width": "100%", "max-width": "300px", "display": "block"}
                        )]
                ),
                html.H4(children="Course Group",
                        style={"justifyContent": "center", "alignItems": "center"}),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            options=course_options,
                            value=options[0]['value'] if options else None,
                            id="course_group_dropdown",
                            style={"width": "100%", "max-width": "300px", "display": "block"}
                        )]
                ),
                html.H4(
                    children="Category",
                    style={"justifyContent": "center", "alignItems": "center"}
                ),
                html.Div(
                    style={"display": "flex", "align-items": "center"},
                    children=[
                        dcc.Dropdown(
                            options=["How good are teaching staff at explaining things?", "How often do teaching staff make the subject engaging?", "How often is the course intellectually stimulating?",
                                     "How often does your course challenge you to achieve your best work?","To what extent does your course have the right balance of directed and independent study?",
                                     "To what extent have you had the chance to explore ideas and concepts in depth?", "How well does your course introduce subjects and skills in a way that builds on what you have already learned?",
                                     "To what extent have you had the chance to bring together information and ideas from different topics",
                                     "How well has your course developed your knowledge and skills that you think you will need for yourfuture?","How clear were the marking criteria used to assess your work?",
                                     "How fair has the marking and assessment been on your course?", "How well have assessments allowed you to demonstrate what you have learned?","How often have you received assessment feedback on time?",
                                     "How often does feedback help you to improve your work?","How easy was it to contact teaching staff when you needed to?","How well have teaching staff supported your learning?",
                                     "How well organised is your course?","How well were any changes to teaching on your course communicated?","How well have the IT resources and facilities supported your learning?",
                                     "How well have the library resources (e.g., books, online services and learning spaces) supported your learning?","How easy is it to access subject specific resources (e.g., equipment, facilities, software) when you need them?",
                                     "To what extent do you get the right opportunities to give feedback on your course?", "To what extent are students' opinions about the course valued by staff?","How clear is it that students' feedback on the course is acted on?",
                                     "How well does the students' union (association or guild) represent students' academic interests? ","I received sufficient preparatory information prior to my placement(s)","I was allocated placement(s) suitable for my course",
                                     "I received appropriate supervision on placement(s)","I was given opportunities to meet my required practice learning outcomes / competences","My contribution during placement(s) as part of the clinical team was valued",
                                     "My practice supervisor(s) understood how my placement(s) related to the broader requirements of my course","Overall, I am satisfied with the quality of the course",
                                     "Looking back on the experience, are there any particularly positive or negative aspects you would like to highlight?","How well communicated was information about your university/college's mental wellbeing support services?",
                                     "During your studies, how free did you feel to express your ideas, opinions, and beliefs?"
                                     ],
                            value="How good are teaching staff at explaining things?",
                            id="questions_dropdown",
                            optionHeight=70,
                            style={"width": "100%", "max-width": "300px", "display": "block"} ,
                        )
                    ]
                ),
                html.H4(children="No of Reviews ",
                        style={"justifyContent": "center",
                               "alignItems": "center", "marginTop": "35px"}
                        ),

                html.Div(
                    style={"marginTop": "30px", "height": "30px", "align-items": "center", "display": "flex"},
                    children=[
                        daq.Slider(
                            id="slider1",
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
                    style={"width": "100%", "alignItems": "center"},
                    children=[
                        html.Button("Submit", id="submit-button", n_clicks=0,
                                        style={
                                        "display": "inline-flex",
                                        "align-items": "center",
                                        "width": "100px",
                                        "height": "40px",
                                        "font-size": "18px",
                                        "border": "none",
                                        "border-radius": "4px",
                                        "background-color": "#007bff",
                                        "color": "#ffffff",
                                        "cursor": "pointer",
                                        "padding": "8px 20px",
                                        "box-shadow": "0px 2px 4px rgba(0, 0, 0, 0.2)",
                                    },
                                    disabled=True)]),
            ]
        ),
        html.Div(
            style={"display": "flex", "align-items": "center",
                   "justify-content": "center"},
            children=[
                dcc.Graph(id="graph", figure=blank_fig(), style={
                    "width": "800px", "height": "500px"})
            ]
        ),
        html.H3(children="Percentage of reviews in each quadrant",
                hidden=True, id="table1_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table1",
            columns=[],
            data=[],
            style_table={"width": "40%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "text-align": "left"
            },
        ),
        html.H3(children="Reviews that are in the Awesome quadrant (Positive feeling with High intensity)",
                hidden=True, id="table_awesome_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table_awesome",
            columns=[],
            data=[],
            style_table={"width": "95%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "width": "auto",
                "text-align": "left"
            },
        ),
        html.H3(children="Reviews that are in the Okay quadrant (Positive feeling with Low intensity)",
                hidden=True, id="table_ok_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table_ok",
            columns=[],
            data=[],
            style_table={"width": "95%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "width": "auto",
                "text-align": "left"
            },
        ),
        html.H3(children="Reviews that are in the Unsatisfactory quadrant (Negative feeling with Low intensity)",
                hidden=True, id="table_unsatis_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table_unsatis",
            columns=[],
            data=[],
            style_table={"width": "95%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "width": "auto",
                "text-align": "left"
            },
        ),
        html.H3(children="Reviews that are in the Terrible quadrant (Negative feeling with High intensity)",
                hidden=True, id="table_terrible_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table_terrible",
            columns=[],
            data=[],
            style_table={"width": "95%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "width": "auto",
                "text-align": "left"
            },
        ),
        html.H3(children="Reviews that are Neutral (on the vertical axis)",
                hidden=True, id="table_nutral_title",style={"margin-left": "30px"}),
        dash_table.DataTable(
            id="table_nutral",
            columns=[],
            data=[],
            style_table={"width": "95%",
                         "marginLeft": "30px", "marginRight": "30px"},
            style_cell={
                "whiteSpace": "normal",
                "height": "auto",
                "width": "auto",
                "text-align": "left"
            },
        )
    ]
)

if __name__ == "__main__":
    PORT = os.getenv("PORT", 8050)
    app.run_server(debug=True, port=PORT, host="0.0.0.0")
