from resources.sim import Scenario, multiple_replications
from treat_sim.distributions import Exponential, Lognormal
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
    n_beds = st.slider('Number of beds', 1, 30, 9, 1)

    #Interarrival time
    stroke_iat = st.slider('Number of beds', 1.0, 20.0, 1.2, 0.1)
    tia_iat = st.slider('Number of beds', 1.0, 20.0, 9.5, 0.1)
    neuro_iat = st.slider('Number of beds', 1.0, 20.0, 3.5, 0.1)
    
    # Treatment time mean
    stroke_treat_mean = st.slider('Number of beds', 1.0, 20.0, 7.4, 0.1)
    tia_treat_mean = st.slider('Number of beds', 1.0, 20.0, 1.8, 0.1)
    neuro_treat_mean = st.slider('Number of beds', 1.0, 20.0, 2.0, 0.1)
    
    # Treatment time std
    stroke_treat_std = st.slider('Number of beds', 1.0, 20.0, 8.5, 0.1)
    tia_treat_std = st.slider('Number of beds', 1.0, 20.0, 2.3, 0.1)
    neuro_treat_std = st.slider('Number of beds', 1.0, 20.0, 2.5, 0.1)
    
    # runs
    replications = st.slider('No. replications', 1, 50, 10)

# Setup scenario using supplied variables
args = Scenario()
args.beds = n_beds

args.arrival_dist_type1 = Exponential(stroke_iat, random_seed=args.seeds[0])
args.arrival_dist_type2 = Exponential(tia_iat, random_seed=args.seeds[1])
args.arrival_dist_type3 = Exponential(neuro_iat, random_seed=args.seeds[2])

args.treatment_dist_type1 = Lognormal(stroke_treat_mean, stroke_treat_std, 
                                      random_seed=args.seeds[3])
args.treatment_dist_type2 = Lognormal(tia_treat_mean, tia_treat_std, 
                                      random_seed=args.seeds[4])
args.treatment_dist_type3 = Lognormal(neuro_treat_mean, neuro_treat_std, 
                                      random_seed=args.seeds[5])

if st.button('Simulate ASU'):

    # in this example run a single replication of the model.
    with st.spinner('Simulating the ASU...'):
        results = multiple_replications(args, n_reps=replications)

    st.success('Done!')

    st.table(results.mean().round(2))

