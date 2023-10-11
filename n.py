import streamlit as st
import sqlite3
from dataclasses import dataclass
##
import streamlit as st
# Set the background color
import base64
st.set_page_config(layout="centered", page_title="My Annotation App", page_icon="favicon.ico")
# Set the background image
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
##
counter = 0

def next():
    st.session_state.counter += 1

def prev():
    st.session_state.counter -= 1

if 'counter' not in st.session_state:
    st.session_state.counter = 0
st.title("Shaper Intern Recruitment Portal")

nickname = st.text_input("NickName")
if nickname:
    st.write(f"Hello {nickname}! Welcome to Shaper. Please fill up the form below:")
questions = ['**### what is your first name**', '### what is your last name']



@dataclass
class Question():
    '''
    Dataclass to store a question and an annotation
    '''
    id: int
    annotation = ""

    def __post_init__(self):
        self.questions = questions

def create_database():
    conn = sqlite3.connect('annotations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS annotations (
        id INTEGER PRIMARY KEY,
        question TEXT,
        annotation TEXT
    )''')
    conn.commit()
    conn.close()

def submit():
    conn = sqlite3.connect('annotations.db')
    c = conn.cursor()

    # Insert the annotations into the database
    for question in st.session_state.my_questions:
        c.execute('INSERT INTO annotations (question, annotation) VALUES (?, ?)', (question.questions[st.session_state.counter%len(questions)], question.annotation))

    conn.commit()
    conn.close()

    # Display a Streamlit success message
    st.success("Your Application  have been successfully submitted to the database!")

if __name__ == "__main__":

    # Create the database if it does not exist
    create_database()

    # Load questions and the current annotation
    if "my_questions" not in st.session_state:
        my_questions = [Question(id=i) for i in range(len(questions))]
        st.session_state.my_questions = my_questions

    else:
        my_questions = st.session_state.my_questions

    n_questions = len(my_questions)

    # App layout
    container = st.empty()
    cols = st.columns(2)
    with cols[1]: st.button("Next", on_click=next, use_container_width=True)
    with cols[0]: st.button("Previous", on_click=prev, use_container_width=True)

    # Fill layout
    with container.container():
        ## Select question based on the current counter
        question = my_questions[st.session_state.counter%n_questions]

        ## Display question
        st.write(question.questions[st.session_state.counter%n_questions])

        ## Get annotation from text_area and allow modification
        text = st.text_input(f"Insert answer for  your question {question.id}:", value=question.annotation)
        question.annotation = text

    # Show state of changes
    with st.sidebar:
        "****"
        "### Debug"
        f" `{st.session_state.counter=}`"
        st.table({question.id : question.annotation for question in my_questions})

    # Display submit button only if all questions have been answered
    if st.session_state.counter == n_questions - 1:
        st.button("Submit", on_click=submit)
        st.info("Thank you for visting our portal we can't wait to meet you!")
        st.warning("Please note that you will get a call from us within the next few days if you are shortlisted,after submitting this form please check your email about the status of your application",icon="⚠️")
