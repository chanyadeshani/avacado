# app.py

import pandas as pd
import os
from dash import Dash, dcc, html, dash_table

import json

data = '''{
  "reviews": [
    {
      "Review": "All good(Smiling face with sunglasses).",
      "similarity": 0.84,
      "valence_score": 0.9,
      "arousal_score": 0.5
    },
    {
      "Review": "All the things are fine.",
      "similarity": 0.81,
      "valence_score": 0.6,
      "arousal_score": 0
    },
    {
      "Review": "Good atmosphere.",
      "similarity": 0.81,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "All okay.",
      "similarity": 0.8,
      "valence_score": 0.2,
      "arousal_score": 0
    },
    {
      "Review": "Friendly faces are always welcoming.",
      "similarity": 0.8,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "Knowledgeable ???.",
      "similarity": 0.79,
      "valence_score": 0.7,
      "arousal_score": 0
    },
    {
      "Review": "Achievement team is really positive. ??? is very helpful.",
      "similarity": 0.79,
      "valence_score": 0.7,
      "arousal_score": 0.5
    },
    {
      "Review": "I have no negative.",
      "similarity": 0.79,
      "valence_score": 1,
      "arousal_score": 0
    },
    {
      "Review": "Nothing.",
      "similarity": 0.79,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "NOTHING",
      "similarity": 0.79,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "I am glad I came to this university.",
      "similarity": 0.79,
      "valence_score": 0.8,
      "arousal_score": 0.1
    },
    {
      "Review": "Had the chance to learn new skills. Had the opportunity to get to know new people in the workplace.",
      "similarity": 0.79,
      "valence_score": 0.5,
      "arousal_score": 0.4
    },
    {
      "Review": "Glad to have been back in real face-to-face lectures and people in the final year have been more sociable.",
      "similarity": 0.78,
      "valence_score": 0.65,
      "arousal_score": 0.6
    },
    {
      "Review": "Great university trips.",
      "similarity": 0.78,
      "valence_score": 0.8,
      "arousal_score": 0.6
    },
    {
      "Review": "Good subjects of study.",
      "similarity": 0.78,
      "valence_score": 0.4,
      "arousal_score": 0
    },
    {
      "Review": "The fellow students are brilliant and supportive.",
      "similarity": 0.78,
      "valence_score": 0.7,
      "arousal_score": 0.3
    },
    {
      "Review": "It is fun learning in university.",
      "similarity": 0.78,
      "valence_score": 0.75,
      "arousal_score": 0.4
    },
    {
      "Review": "Don't know.",
      "similarity": 0.78,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "Made good friends and connections, had good experiences that will help me in the future. Learned a lot about living independently and finance management. Learned how to balance multiple workloads with social responsibilities.",
      "similarity": 0.78,
      "valence_score": 0.8,
      "arousal_score": 0.8
    },
    {
      "Review": "Staff are friendly and helpful mostly.",
      "similarity": 0.78,
      "valence_score": 0.5,
      "arousal_score": 0.1
    },
    {
      "Review": "Staff are great.",
      "similarity": 0.78,
      "valence_score": 0.7,
      "arousal_score": 0.1
    },
    {
      "Review": "NO NOT PARTICULARY",
      "similarity": 0.78,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "Good mates made, course has many aspects and topics to look into in-depth.",
      "similarity": 0.78,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "Good friends made, small classroom and easier to get help and discuss issues. Topics given are very interesting.",
      "similarity": 0.78,
      "valence_score": 0.76,
      "arousal_score": 0.6
    },
    {
      "Review": "Generally positive approach from staff towards teaching. Mostly a good level of support for students.",
      "similarity": 0.78,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "They transitioned well in terms of COVID right now.",
      "similarity": 0.77,
      "valence_score": 0.4,
      "arousal_score": 0
    },
    {
      "Review": "Fun, great learning experience, a lot to learn and they teach you very well.",
      "similarity": 0.77,
      "valence_score": 0.8,
      "arousal_score": 0.8
    },
    {
      "Review": "Learnt a lot of skills and developed his/her mind.",
      "similarity": 0.77,
      "valence_score": 0.65,
      "arousal_score": 0.5
    },
    {
      "Review": "Good assistance, a lot of help, good guidance.",
      "similarity": 0.77,
      "valence_score": 0.7,
      "arousal_score": 0.3
    },
    {
      "Review": "Results of the assignment are pretty good most of the time, except for one or two assignments.",
      "similarity": 0.77,
      "valence_score": 0.3,
      "arousal_score": 0.1
    },
    {
      "Review": "Staff are doing much better now during the pandemic, some of which being more accessible than beforehand.",
      "similarity": 0.77,
      "valence_score": 0.55,
      "arousal_score": 0.4
    },
    {
      "Review": "Had the opportunity to go on placement.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0
    },
    {
      "Review": "Friendly helper lecturing staff make the course fun and enjoyable. The course is fun but challenging.",
      "similarity": 0.77,
      "valence_score": 0,
      "arousal_score": 0.8
    },
    {
      "Review": "Wish there were more trips.",
      "similarity": 0.77,
      "valence_score": 0.3,
      "arousal_score": 0.1
    },
    {
      "Review": "Some of the extracurricular events and activities provided were really fun and helpful.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "Teachers are good. The course itself is very good. It's very positive overall.",
      "similarity": 0.77,
      "valence_score": 0.9,
      "arousal_score": 0.5
    },
    {
      "Review": "The lecturers are interested in your well-being.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "Waking up early.",
      "similarity": 0.77,
      "valence_score": 0,
      "arousal_score": -0.5
    },
    {
      "Review": "Tutors are friendly, sometimes they check up, they are upbeat, senior staff are more friendly and caring, considerate of the student's wellbeing, they are friendly.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0.5
    },
    {
      "Review": "Mostly everything.",
      "similarity": 0.77,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "Placement was fantastic.",
      "similarity": 0.77,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "Being provided with various resources is very helpful and great information.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0.3
    },
    {
      "Review": "The course is challenging, a good one product.",
      "similarity": 0.77,
      "valence_score": 0.5,
      "arousal_score": 0.5
    },
    {
      "Review": "Great feedback.",
      "similarity": 0.77,
      "valence_score": 0.9,
      "arousal_score": 0.3
    },
    {
      "Review": "Communication between lecturers and students. Help and support. Friendly working environments. Enjoyable modules. Good support services to assist with assignments and mental health.",
      "similarity": 0.77,
      "valence_score": 0.7,
      "arousal_score": 0.8
    },
    {
      "Review": "Having access to the Adobe software at home is a great.",
      "similarity": 0.77,
      "valence_score": 0.9,
      "arousal_score": 0.1
    },
    {
      "Review": "I feel like I've been given the correct guidance to complete my course to the best of my ability.",
      "similarity": 0.77,
      "valence_score": 0.7,
      "arousal_score": 0.1
    },
    {
      "Review": "The lecturers are really and they are good at making you excited for the assignments.",
      "similarity": 0.77,
      "valence_score": 0.8,
      "arousal_score": 0.6
    },
    {
      "Review": "Able to get support from lecturers easily.",
      "similarity": 0.77,
      "valence_score": 0.6,
      "arousal_score": 0.5
    },
    {
      "Review": "Awesome staff and modules.",
      "similarity": 0.76,
      "valence_score": 0.9,
      "arousal_score": 0.8
    },
    {
      "Review": "Staff genuinely enjoy what they are teaching and the passion really shows.",
      "similarity": 0.76,
      "valence_score": 0.85,
      "arousal_score": 0.4
    },
    {
      "Review": "The class sizes are not too big so feel we feel engaged.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.4
    },
    {
      "Review": "Great lectures. Interesting assignments.",
      "similarity": 0.76,
      "valence_score": 0.85,
      "arousal_score": 0.4
    },
    {
      "Review": "Some positive and understanding lecturers. Some enthusiastic lecturers. Some good modules. Interesting and practicals are relevant and quality (interest in new things, Arduinos for example).",
      "similarity": 0.76,
      "valence_score": 0.2,
      "arousal_score": 0.5
    },
    {
      "Review": "The range of topics was interesting and useful.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.1
    },
    {
      "Review": "Opportunity to work with other student. The staff members treat you with respect and dignity when you present them with an issue.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.5
    },
    {
      "Review": "Lots of room for creativity.",
      "similarity": 0.76,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "There have been a few hiccups this year, modules and organisation fell apart a bit. We didn't have the tools we needed briefly, but we got them back again.",
      "similarity": 0.76,
      "valence_score": 0.3,
      "arousal_score": 0
    },
    {
      "Review": "The computers and the resources are good and will usually have a site free to work.",
      "similarity": 0.76,
      "valence_score": 0.4,
      "arousal_score": 0.1
    },
    {
      "Review": "Support from tutor has been good in both academic and pastoral work.",
      "similarity": 0.76,
      "valence_score": 0.65,
      "arousal_score": 0.6
    },
    {
      "Review": "They really supported us on final project and paid for hotel when we go away, supportive, love talking to my lecturers, lovely people.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.4
    },
    {
      "Review": "Careers support.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "The new grading grids have been very helpful to identify how to improve grades. Staff are always very supportive, offering good guidance. I feel the work that I get to do enhance my portfolio and is very useful.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0.5
    },
    {
      "Review": "Nothing stands out.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "Ever since the pandemic, lecturers have been more active when it comes to communicating with students. Lecturers are always happy to have a chat whether it is in a group or in a one-to-one setting.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.6
    },
    {
      "Review": "I've been given the opportunity to be independent to a great extent.",
      "similarity": 0.76,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "Everybody is helpful that is undeniable and if I am in trouble I can always get help.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.6
    },
    {
      "Review": "Variety of topics discussed.",
      "similarity": 0.76,
      "valence_score": 0.5,
      "arousal_score": 0
    },
    {
      "Review": "Lecturer student interaction/relationship has been excellent. Excellent library materials.",
      "similarity": 0.76,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "Being given the opportunity to work as part of a group for projects I found was extremely beneficial to both study and social aspects of University life.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.6
    },
    {
      "Review": "Interesting course. Fantastic library team. Fantastic 'your future plan' team (careers). Brilliant support teams and chaplaincy team. Lovely campus. Good attitude to the environment.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0.5
    },
    {
      "Review": "There is a mutual respect between staff and students.",
      "similarity": 0.76,
      "valence_score": 0.65,
      "arousal_score": 0.1
    },
    {
      "Review": "Providing students with access to the Adobe Suite of software has been really helpful, allowing students to work on projects that need Adobe software to work from home as well as on campus. Organized social events for the course have been good.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.5
    },
    {
      "Review": "The lecturers are very supportive. The facilities are well maintained.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.4
    },
    {
      "Review": "Game Jam and games night were the best moments, taking what you have learned and putting it to the test.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.8
    },
    {
      "Review": "Placement opportunities.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "There are a couple of lecturers that are outstanding; they are both academically and emotionally supportive and easy to speak with.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.9
    },
    {
      "Review": "The University experience as a whole was very good and the lecturers were all good.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.4
    },
    {
      "Review": "??? has been a fantastic lecturer and goes above and beyond!",
      "similarity": 0.76,
      "valence_score": 0.8,
      "arousal_score": 0.6
    },
    {
      "Review": "Lots of coverage, really helpful and friendly staff, plenty of opportunities to try out different fields and see what your careers need to be. ??? is really helpful, engaging and knowledgeable.",
      "similarity": 0.76,
      "valence_score": 0,
      "arousal_score": 0.8
    },
    {
      "Review": "Academic ??? has been helpful throughout my time here; he/she has given me support and advice when needed.",
      "similarity": 0.76,
      "valence_score": 0.5,
      "arousal_score": 0.1
    },
    {
      "Review": "Interactive staff. Able to openly talk to staff regarding course problems. ??? is very helpful. Integrated placement year.",
      "similarity": 0.76,
      "valence_score": 0.7,
      "arousal_score": 0.5
    },
    {
      "Review": "The time I spent with people in my lectures.",
      "similarity": 0.76,
      "valence_score": 0.5,
      "arousal_score": 0.1
    },
    {
      "Review": "Lecture wise the staff are friendly; they are there for the students in the lectures.",
      "similarity": 0.76,
      "valence_score": 0.4,
      "arousal_score": 0.6
    },
    {
      "Review": "Most lecturers have good communication with students when help was needed during deadline season.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.6
    },
    {
      "Review": "Helpful staff when trying to get advice about what to do regarding some medical issues that I have had.",
      "similarity": 0.76,
      "valence_score": 0.4,
      "arousal_score": 0.4
    },
    {
      "Review": "The topics and concepts shown in the course were interesting and appealing.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.5
    },
    {
      "Review": "Lecturers are really friendly and willing to help.",
      "similarity": 0.76,
      "valence_score": 0.75,
      "arousal_score": 0.5
    },
    {
      "Review": "Course teething problems.",
      "similarity": 0.76,
      "valence_score": -0.4,
      "arousal_score": 0
    },
    {
      "Review": "Some of the staff in particular are a pleasure to be lectured by.",
      "similarity": 0.76,
      "valence_score": 0.55,
      "arousal_score": 0.5
    },
    {
      "Review": "Tutors are very approachable when needed.",
      "similarity": 0.76,
      "valence_score": 0.5,
      "arousal_score": 0.5
    },
    {
      "Review": "Good individual lecturers who care and help me learn.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.1
    },
    {
      "Review": "N/A. Been quite varied in what we've been able to do, give a lot of freedom.",
      "similarity": 0.76,
      "valence_score": 0.6,
      "arousal_score": 0.5
    },
    {
      "Review": "Good lecturer's feedback on assignments. Application of Agile working, present in group work projects.",
      "similarity": 0.75,
      "valence_score": 0.8,
      "arousal_score": 0.5
    },
    {
      "Review": "What I have gained learned and lost.",
      "similarity": 0.75,
      "valence_score": 0,
      "arousal_score": 0
    },
    {
      "Review": "??? was amazing. SU improved massively and was a great support. Helpzone and future plan were useful and good resources.",
      "similarity": 0.75,
      "valence_score": 0.8,
      "arousal_score": 0
    },
    {
      "Review": "I did pick up some decent digital skills which I wouldn't have gained going to art college. The ??? mentor and the ??? mentor were both nice and I got biscuits and memory sticks when I needed them from the ??? mentor.",
      "similarity": 0.75,
      "valence_score": 0.7,
      "arousal_score": 0.6
    },
    {
      "Review": "The topics studied have been interesting for the most part, and I have seen a great improvement in my skills over the course.",
      "similarity": 0.75,
      "valence_score": 0.75,
      "arousal_score": 0.5
    },
    {
      "Review": "Overall teachers are very helpful.",
      "similarity": 0.75,
      "valence_score": 0.6,
      "arousal_score": 0.1
    },
    {
      "Review": "All lecturers are friendly, helpful, and knowledgeable. They're always readily able to help and provide true feedback, as well as join us at socials. Really friendly course with the students and their progress at the focus.",
      "similarity": 0.75,
      "valence_score": 0.8,
      "arousal_score": 0.8
    }
  ],
  "emotion_states": [
    "coming soon..."
  ]
}
'''


dict = json.loads(data)
# Extract the "reviews" data
reviews_data = dict["reviews"]

# Convert to Pandas DataFrame
df = pd.DataFrame(reviews_data)

app = Dash(__name__)

app.layout = html.Div(
        style={ "justify-content": "center"},  # Center the graph horizontally
    children=[
        html.H1(children="National Student Suervey"),
        html.P(
            children=(
                "Analysis of student comments"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["valence_score"],
                        "y": df["arousal_score"],
                        "mode": "markers",
                    },
                ],
                "layout": {
                    "title": "Valence and Arousal",
                    "width": 800,  # Set the width of the figure
                    "height": 500,  # Set the height of the figure
                },
            },
        ),
        dash_table.DataTable(
            id="table",
            columns=[{"name": col, "id": col} for col in df.columns[:2]],  # Only display first two columns
            data=df.to_dict("records"), 
            style_table={"width": "80%"},
            style_cell={
                "maxWidth": "20px",  # Limiting cell width to 20 characters
                "overflow": "hidden",
                "textOverflow": "ellipsis",
            },
        ),
    ]
)
if __name__ == "__main__":
    PORT = os.getenv('PORT', 8050)
    app.run_server(debug=True, port=PORT, host="0.0.0.0")
