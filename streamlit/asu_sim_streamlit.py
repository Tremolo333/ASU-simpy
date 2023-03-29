from resources.sim import Scenario, multiple_replications
import streamlit as st
import glob
import os

INTRO_FILE = 'resources/overview.md'

def read_file_contents(file_name):
    ''''
    Read the contents of a file.

    Params:
    ------
    file_name: str
        Path to file.

    Returns:
    -------
    str
    '''
    with open(file_name) as f:
        return f.read()

# give the page a title
st.title('Acute Stroke Unit (ASU) Simulation Model')

# show the introductory markdown
st.markdown(read_file_contents(INTRO_FILE))

# Using "with" notation
with st.sidebar:

    # set the variables for the run.
    # these are just a subset of the total available for this example...
    # in streamlit we are going to set these using sliders.
    triage_bays = st.slider('Triage bays', 1, 5, 1)
    exam_rooms = st.slider('Exam rooms', 1, 5, 3)
    treat_rooms = st.slider('Non-Trauma Treatment cubicles', 1, 5, 1, 
                            help='Set the number of non trauma pathway treatment cubicles')

    # examination mean
    exam_mean = st.slider('Mean examination time', 10.0, 45.0, 
                        16.0, 1.0)

    # runs
    replications = st.slider('No. replications', 1, 50, 10)

# Setup scenario using supplied variables
args = Scenario()
args.n_triage = triage_bays
args.n_exam = exam_rooms
args.n_cubicles_1 = treat_rooms
args.exam_mean = exam_mean

if st.button('Simulate ASU'):

    # in this example run a single replication of the model.
    with st.spinner('Simulating the ASU...'):
        results = multiple_replications(args, n_reps=replications)

    st.success('Done!')

    st.table(results.mean().round(2))

