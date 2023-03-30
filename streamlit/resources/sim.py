#simulation model

import numpy as np
import pandas as pd
import itertools
import math
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
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

# run length in days
RUN_LENGTH = 365

# default № of reps for multiple reps run
DEFAULT_N_REPS = 5

# default random number SET
DEFAULT_RNG_SET = None
N_STREAMS = 10

# Turn off tracing
TRACE = False 

# resource counts
N_BEDS = 9

# time between arrivals in minutes (exponential)
# for acute stroke, TIA and neuro respectively
MEAN_IATs = [1.2, 9.5, 3.5]

# treatment (lognormal)
# for acute stroke, TIA and neuro respectively
TREAT_MEANs = [7.4, 1.8, 2.0]
TREAT_STDs = [8.5, 2.3, 2.5]

# SEEDS to reproduce results of a single run
REPRODUCIBLE_RUN = False
    
if REPRODUCIBLE_RUN:
    SEEDS = [42, 101, 1066, 1966, 2013, 999, 1444, 2016]
else:
    SEEDS = [None, None, None, None, None, None, None, None]


# Scenario class
class Scenario:
    '''
    Parameter container class for minor injury unit model.
    '''
    def __init__(self, random_number_set=DEFAULT_RNG_SET):
        '''
        The init method sets up our defaults. 
        
        Params:
        -------
        
        name - str or None
            optional name for scenario
        '''
        
        # warm-up
        self.warm_up = 0.0

        # sampling
        self.random_number_set = random_number_set
        self.init_sampling()
        
        # number of beds
        self.beds = N_BEDS
        
        
    def set_random_no_set(self, random_number_set):
        '''
        Controls the random sampling 

        Parameters:
        ----------
        random_number_set: int
            Used to control the set of psuedo random numbers
            used by the distributions in the simulation.
        '''
        self.random_number_set = random_number_set
        self.init_sampling()
        
        
    def init_sampling(self):
        '''
        Create the distributions used by the model and initialise 
        the random seeds of each.
        '''
        # create random number streams
        rng_streams = np.random.default_rng(self.random_number_set)
        self.seeds = rng_streams.integers(0, 999999999, size=N_STREAMS)


        # inter-arrival distributions
        self.arrival_dist_type1 = Exponential(MEAN_IATs[0], random_seed=self.seeds[0])
        self.arrival_dist_type2 = Exponential(MEAN_IATs[1], random_seed=self.seeds[1])
        self.arrival_dist_type3 = Exponential(MEAN_IATs[2], random_seed=self.seeds[2])
        
        
        # treatment distributions
        self.treatment_dist_type1 = Lognormal(TREAT_MEANs[0], TREAT_STDs[0], 
                                              random_seed=self.seeds[3])
        self.treatment_dist_type2 = Lognormal(TREAT_MEANs[1], TREAT_STDs[1], 
                                              random_seed=self.seeds[4])
        self.treatment_dist_type3 = Lognormal(TREAT_MEANs[2], TREAT_STDs[2], 
                                              random_seed=self.seeds[5])
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
        self.treat_time = 0.0
        
    
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
            self.treat_time = self.treatment_dist_type1.sample()
            
            activity_duration = self.treat_time
          
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
            self.treat_time = self.treatment_dist_type2.sample()
            
            activity_duration = self.treat_time
          
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
            self.treat_time = self.treatment_dist_type3.sample()
            
            activity_duration = self.treat_time
          
            # treatment delay
            yield self.env.timeout(activity_duration)
            
class ASU:  
    '''
    Model of an ASU
    '''
    def __init__(self, args):
        '''
        Contructor
        
        Params:
        -------
        env: simpy.Environment
        
        args: Scenario
            container class for simulation model inputs.
        '''
        self.env = simpy.Environment()
        self.args = args 
        self.init_model_resources(args)
        self.patients = []
        self.patient_count = 0
        self.type1_count = 0
        self.type2_count = 0
        self.type3_count = 0
        
        
    def init_model_resources(self, args):
        '''
        Setup the simpy resource objects
        
        Params:
        ------
        args - Scenario
            Simulation Parameter Container
        '''

        self.args.beds = simpy.Resource(self.env, 
                                   capacity=9999999)
        
        
    def run(self, results_collection_period = RUN_LENGTH,
            warm_up = 0):
        '''
        Conduct a single run of the model in its current 
        configuration

        run length = results_collection_period + warm_up

        Parameters:
        ----------
        results_collection_period, float, optional
            default = RUN_LENGTH

        warm_up, float, optional (default=0)
            length of initial transient period to truncate
            from results.

        Returns:
        --------
            None

        '''
        # setup the arrival processes
        self.env.process(self.arrivals_generator_type1())
        self.env.process(self.arrivals_generator_type2())
        self.env.process(self.arrivals_generator_type3())
                
        # run
        self.env.run(until=results_collection_period+warm_up)
        
            
    def arrivals_generator_type1(self):
            
        while True:
            
            
                # PATIENT WITH ACUTE STROKE ARRIVES (TYPE 1)
                inter_arrival_time = self.args.arrival_dist_type1.sample()               
                
                yield self.env.timeout(inter_arrival_time)
                
                self.patient_count += 1
                self.type1_count += 1
                
                trace(f'Patient № {self.patient_count} (Stroke) arrives at: {self.env.now:.3f}')
                
                # create a new patient and pass in env and args
                new_patient = Patient(self.patient_count, self.env, self.args)                

                # init the minor injury process for this patient
                self.env.process(new_patient.treatment_type1())                 
            
                # keep a record of the patient for results calculation
                self.patients.append(new_patient)                
                
                
    def arrivals_generator_type2(self):
            
        while True:
            
                            
                # PATIENT WITH TRANSITORY ISCHEMIC ATTACK ARRIVES (TYPE 2)
                inter_arrival_time = self.args.arrival_dist_type2.sample()
           
                yield self.env.timeout(inter_arrival_time)
            
                self.patient_count += 1
                self.type2_count += 1
                                
                trace(f'Patient № {self.patient_count} (TIA) arrives at: {self.env.now:.3f}')   
                
                # create a new patient and pass in env and args
                new_patient = Patient(self.patient_count, self.env, self.args)
            
                # init the minor injury process for this patient
                self.env.process(new_patient.treatment_type2())                
                
                # keep a record of the patient for results calculation
                self.patients.append(new_patient)                
                
    def arrivals_generator_type3(self):
            
        while True:
            
                
                # PATIENT WITH COMPLEX NEUROLOGICAL DIAGNOSIS ARRIVES (TYPE 3)
                inter_arrival_time = self.args.arrival_dist_type3.sample()
                
                yield self.env.timeout(inter_arrival_time)
                
                self.patient_count += 1
                self.type3_count += 1
                
                trace(f'Patient № {self.patient_count} (Neuro) arrives at: {self.env.now:.3f}')
                
                # create a new patient and pass in env and args
                new_patient = Patient(self.patient_count, self.env, self.args)
            
                # init the minor injury process for this patient
                self.env.process(new_patient.treatment_type3())                
                
                # keep a record of the patient for results calculation
                self.patients.append(new_patient)
                
    def run_summary_frame(self):
        
        '''
        Utility function for final metrics calculation.
        
        Returns df containining
        mean waiting time of the bottom 90% of the pts
        formatted to hours and bed util
        '''
        # np array of all queue times to treatment
        patients_queue_times = np.array([patient.queue_time 
                                   for patient in self.patients])

        # transform values from days into hours
        patients_queue_times *= 24
    
        # calculate total number of patients
        arr_length = np.size(patients_queue_times)

        # determine the number of values to be dropped
        num_to_drop = int(arr_length * 0.1)

        # sort the array in descending order
        sorted_queue_times = np.sort(patients_queue_times)[::-1]

        # drop top 10%, estimate the mean
        queue_bottom90 = sorted_queue_times[num_to_drop:].mean()
    
    
        #bed utilisation = sum(call durations) / (run length X no. BEDS)
        util = np.array([patient.treat_time 
                     for patient in self.patients]).sum() / (RUN_LENGTH * N_BEDS)
        
        average_treat_time = np.array([patient.treat_time 
                     for patient in self.patients]).sum() / self.patient_count
        

        df = pd.DataFrame({'1':{'1b Stroke Patient Arrivals':self.type1_count,
                                '2 Bottom 90% Mean Treatment Waiting Time (hrs)': queue_bottom90, 
                                '3 Bed Utilisation (%)': util*100,
                                '1a Total Patient Arrivals':self.patient_count,
                                '1d Neuro Patient Arrivals':self.type3_count,
                                '1c TIA Patient Arrivals':self.type2_count,
                                '4 Mean Total Time in Unit per patient(hrs)':average_treat_time}})
        
        df = df.T
        df.index.name = 'rep'
        return df

#Functions for single and multiple runs
def single_run(scenario, rc_period = RUN_LENGTH, 
               warm_up = 0, random_no_set = DEFAULT_RNG_SET):
    '''
    Perform a single run of the model and return the results
    
    Parameters:
    -----------
    
    scenario: Scenario object
        The scenario/paramaters to run
        
    rc_period: int
        The length of the simulation run that collects results
        
    warm_up: int, optional (default=0)
        warm-up period in the model.  The model will not collect any results
        before the warm-up period is reached.  
        
    random_no_set: int or None, optional (default=1)
        Controls the set of random seeds used by the stochastic parts of the 
        model.  Set to different ints to get different results.  Set to None
        for a random set of seeds.
        
    Returns:
    --------
        pandas.DataFrame:
        results from single run.
    '''  
        
    # set random number set - this controls sampling for the run.
    scenario.set_random_no_set(random_no_set)
    
    # create the model
    model = ASU(scenario)

    model.run(results_collection_period = rc_period, warm_up = warm_up)
    
    # run the model
    results_summary= model.run_summary_frame()
    
    return results_summary

def multiple_replications(scenario, rc_period=RUN_LENGTH, warm_up=0,
                          n_reps=DEFAULT_N_REPS, n_jobs=-1):
    '''
    Perform multiple replications of the model.
    
    Params:
    ------
    scenario: Scenario
        Parameters/arguments to configurethe model
    
    rc_period: float, optional (default=DEFAULT_RESULTS_COLLECTION_PERIOD)
        results collection period.  
        the number of minutes to run the model beyond warm up
        to collect results
    
    warm_up: float, optional (default=0)
        initial transient period.  no results are collected in this period

    n_reps: int, optional (default=DEFAULT_N_REPS)
        Number of independent replications to run.

    n_jobs, int, optional (default=-1)
        No. replications to run in parallel.
        
    Returns:
    --------
    List
    '''    
    res = Parallel(n_jobs=n_jobs)(delayed(single_run)(scenario, 
                                                      rc_period, 
                                                      warm_up,
                                                      random_no_set=rep) 
                                  for rep in range(n_reps))


    # format and return results in a dataframe
    df_results = pd.concat(res)
    df_results.index = np.arange(1, len(df_results)+1)
    df_results.index.name = 'rep'
    return df_results


