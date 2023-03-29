#simulation model

import numpy as np
import pandas as pd
import itertools
import math
import matplotlib.pyplot as plt
import simpy
from treat_sim.distributions import Exponential, Lognormal


# Utility function
def trace(msg):
    '''
    Utility function for printing simulation
    set the TRACE constant to FALSE to 
    turn tracing off.
    
    Params:
    -------
    msg: str
        string to print to screen.
    '''
    if TRACE:
        print(msg)

# Distribution parameters

# These are the parameters for a base case model run.
# Note if you change these parameters then your model will run a new 'scenario' 

# resource counts
DEFAULT_N_BEDS = 9

# time between arrivals in minutes (exponential)
# for acute stroke, TIA and neuro respectively
DEFAULT_MEAN_IATs = [1.2, 9.5, 3.5]

# treatment (lognormal)
# for acute stroke, TIA and neuro respectively
DEFAULT_TREAT_MEANs = [7.4, 1.8, 2.0]
DEFAULT_TREAT_STDs = [8.5, 2.3, 2.5]

# SEEDS to reproduce results of a single run
REPRODUCIBLE_RUN = True
    
if REPRODUCIBLE_RUN:
    SEEDS = [42, 101, 1066, 1966, 2013, 999, 1444, 2016]
else:
    SEEDS = [None, None, None, None, None, None, None, None]

# Show the a trace of simulated events
# not recommended when running multiple replications
TRACE = False

# list of metrics useful for external apps
RESULT_FIELDS = ['00a_total_arrivals',
                 '00b_stroke_arrivals',
                 '00c_TIA_arrivals',
                 '00d_Neuro_arrivals',
                 '04a_treatment_wait',
                 '04b_treatment_util',
                 '05_total_time',
                 '09_throughput']

# list of metrics useful for external apps
RESULT_LABELS = {'00_arrivals': 'Total arrivals',
                 '00b_stroke_arrivals': 'Stroke arrivals',
                 '00c_TIA_arrivals': 'TIA arrivals',
                 '00d_Neuro_arrivals': 'Neuro arrivals',
                 '04a_treatment_wait': 'Treatment waiting time (mins)',
                 '04b_treatment_util': 'Bed utilisation',
                 '05_total_time': 'Total time',
                 '09_throughput': 'throughput'}    
    
    
# Model parameterisation
class Scenario:
    '''
    Container class for scenario parameters/arguments
    For convienience a container class is used to hold the large number of model 
    parameters.  
    
    The `Scenario` class includes defaults, these can easily be 
    changed and at runtime to experiments with different designs.
    
    Passed to a model and its process classes
    '''
    def __init__(self, name = None):
        '''
        The init method sets up our defaults. 
        
        Params:
        -------
        
        name - str or None
            optional name for scenario
        '''
        # optional name
        self.name = name
        
        # number of beds
        self.beds = DEFAULT_N_BEDS
        
        # inter-arrival distributions
        self.arrival_dist_type1 = Exponential(DEFAULT_MEAN_IATs[0], random_seed=SEEDS[0]) 
        self.arrival_dist_type2 = Exponential(DEFAULT_MEAN_IATs[1], random_seed=SEEDS[1])
        self.arrival_dist_type3 = Exponential(DEFAULT_MEAN_IATs[2], random_seed=SEEDS[2])
        
        
        # treatment distributions
        self.treatment_dist_type1 = Lognormal(DEFAULT_TREAT_MEANs[0], 
                                              DEFAULT_TREAT_STDs[0], random_seed=SEEDS[3])
        self.treatment_dist_type2 = Lognormal(DEFAULT_TREAT_MEANs[1], 
                                              DEFAULT_TREAT_STDs[1], random_seed=SEEDS[4])
        self.treatment_dist_type3 = Lognormal(DEFAULT_TREAT_MEANs[2], 
                                              DEFAULT_TREAT_STDs[2], random_seed=SEEDS[5])
# Model building        
class Patient:
    '''
    Patient in the minor ED process
    '''
    def __init__(self, identifier, env, args):
        '''
        Constructor method
        
        Params:
        -----
        identifier: int
            a numeric identifier for the patient.
            
        env: simpy.Environment
            the simulation environment
            
        args: Scenario
            The input data for the scenario
        '''
        # patient id and environment
        self.identifier = identifier
        self.env = env

        # treatment parameters
        self.beds = args.beds
        self.treatment_dist_type1 = args.treatment_dist_type1
        self.treatment_dist_type2 = args.treatment_dist_type2
        self.treatment_dist_type3 = args.treatment_dist_type3
                
        # individual patient metrics
        self.queue_time = 0.0
        
    
    def treatment_type1(self):

        # record the time that patient entered the system
        arrival_time = self.env.now
     
        # get a bed
        with self.beds.request() as req:
            yield req
            
            # record time to first being seen by a doctor
            self.queue_time = self.env.now - arrival_time
                        
            trace(f'Patient № {self.identifier} started treatment at {self.env.now:.3f};'
                      + f' queue time was {self.queue_time:.3f}')

            # sample for patient pathway
            treat_time = self.treatment_dist_type1.sample()
            
            activity_duration = treat_time
          
            # treatment delay
            yield self.env.timeout(activity_duration)

            
            
    def treatment_type2(self):

        # record the time that patient entered the system
        arrival_time = self.env.now
     
        # get a bed
        with self.beds.request() as req:
            yield req
            
            # record time to first being seen by a doctor
            self.queue_time = self.env.now - arrival_time
                        
            trace(f'Patient № {self.identifier} started treatment at {self.env.now:.3f};'
                      + f' queue time was {self.queue_time:.3f}')

            # sample for patient pathway
            treat_time = self.treatment_dist_type2.sample()
            
            activity_duration = treat_time
          
            # treatment delay
            yield self.env.timeout(activity_duration)
                        
            
            
            
    def treatment_type3(self):

        # record the time that patient entered the system
        arrival_time = self.env.now
     
        # get a bed
        with self.beds.request() as req:
            yield req
            
            # record time to first being seen by a doctor
            self.queue_time = self.env.now - arrival_time
                        
            trace(f'Patient № {self.identifier} started treatment at {self.env.now:.3f};'
                      + f' queue time was {self.queue_time:.3f}')

            # sample for patient pathway
            treat_time = self.treatment_dist_type3.sample()
            
            activity_duration = treat_time
          
            # treatment delay
            yield self.env.timeout(activity_duration)
