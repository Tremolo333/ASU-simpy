
import numpy as np
import pandas as pd
import itertools
import math
import matplotlib.pyplot as plt
import simpy
from joblib import Parallel, delayed
#from treat_sim.distributions import Exponential, Lognormal


# Distribution classes


class Exponential:
    '''
    Convenience class for the exponential distribution.
    packages up distribution parameters, seed and random generator.
    '''
    def __init__(self, mean, random_seed=None):
        '''
        Constructor
        
        Params:
        ------
        mean: float
            The mean of the exponential distribution
        
        random_seed: int, optional (default=None)
            A random seed to reproduce samples.  If set to none then a unique
            sample is created.
        '''
        self.rand = np.random.default_rng(seed=random_seed)
        self.mean = mean
        
    def sample(self, size=None):
        '''
        Generate a sample from the exponential distribution
        
        Params:
        -------
        size: int, optional (default=None)
            the number of samples to return.  If size=None then a single
            sample is returned.
        '''
        return self.rand.exponential(self.mean, size=size)

class Lognormal:
    """
    Encapsulates a lognormal distirbution
    """
    def __init__(self, mean, stdev, random_seed=None):
        """
        Params:
        -------
        mean = mean of the lognormal distribution
        stdev = standard dev of the lognormal distribution
        """
        self.rand = np.random.default_rng(seed=random_seed)
        mu, sigma = self.normal_moments_from_lognormal(mean, stdev**2)
        self.mu = mu
        self.sigma = sigma
        
    def normal_moments_from_lognormal(self, m, v):
        '''
        Returns mu and sigma of normal distribution
        underlying a lognormal with mean m and variance v
        source: https://blogs.sas.com/content/iml/2014/06/04/simulate-lognormal
        -data-with-specified-mean-and-variance.html

        Params:
        -------
        m = mean of lognormal distribution
        v = variance of lognormal distribution
                
        Returns:
        -------
        (float, float)
        '''
        phi = math.sqrt(v + m**2)
        mu = math.log(m**2/phi)
        sigma = math.sqrt(math.log(phi**2/m**2))
        return mu, sigma
        
    def sample(self):
        """
        Sample from the normal distribution
        """
        return self.rand.lognormal(self.mu, self.sigma)


# Utility functions


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


# Model parameters

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
N_BEDS = 10

# time between arrivals in minutes (exponential)
# for acute stroke, TIA and neuro respectively
MEAN_IATs = [1.2, 9.5, 3.5]

# treatment (lognormal)
# for acute stroke, TIA and neuro respectively
TREAT_MEANs = [7.4, 1.8, 2.0]
TREAT_STDs = [8.5, 2.3, 2.5]


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
        
        # either hard-coded or obtained from streamlit
        self.iat_means = MEAN_IATs
        self.treat_means = TREAT_MEANs
        self.treat_stds = TREAT_STDs

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
        
        
        # inter-arrival distributions samples
        self.arrival_dist_samples = {
            'stroke': Exponential(self.iat_means[0], random_seed=self.seeds[0]),
            'tia': Exponential(self.iat_means[1], random_seed=self.seeds[1]),
            'neuro': Exponential(self.iat_means[2], random_seed=self.seeds[2])
        }
        
        # treatment distributions samples
        self.treatment_dist_samples = {
            'stroke': Lognormal(self.treat_means[0], self.treat_stds[0], random_seed=self.seeds[3]),
            'tia': Lognormal(self.treat_means[1], self.treat_stds[1], random_seed=self.seeds[4]),
            'neuro': Lognormal(self.treat_means[2], self.treat_stds[2], random_seed=self.seeds[5])
        }
            
        


# Model building

class Patient:
    '''
    Patient in the minor ED process
    '''
    def __init__(self, identifier, patient_type, env, args):
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
        
        self.patient_type = patient_type

        # treatment parameters
        self.beds = args.beds
        self.treatment_dist_samples = args.treatment_dist_samples
                
        # individual patient metrics
        self.queue_time = 0.0
        self.treat_time = 0.0
        
    def get_treatment_dist_sample(self):

        # sample for patient pathway
        if self.patient_type == 'stroke':
            self.treat_time = self.treatment_dist_samples['stroke'].sample()
        elif self.patient_type == 'tia':
            self.treat_time = self.treatment_dist_samples['tia'].sample()
        else:
            self.treat_time = self.treatment_dist_samples['neuro'].sample()  
                
        activity_duration = self.treat_time
            
        return activity_duration
        
    
    def treatment(self):

        # record the time that patient entered the system
        arrival_time = self.env.now
     
        # get a bed
        with self.beds.request() as req:
            yield req
            
            # record time to first being seen by a doctor
            self.queue_time = self.env.now - arrival_time

            trace(f'Patient № {self.identifier} started treatment at {self.env.now:.3f};'
                      + f' queue time was {self.queue_time:.3f}')            

            # treatment delay
            yield self.env.timeout(self.get_treatment_dist_sample())


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
        self.stroke_count = 0
        self.tia_count = 0
        self.neuro_count = 0
        
        
    def init_model_resources(self, args):
        '''
        Setup the simpy resource objects
        
        Params:
        ------
        args - Scenario
            Simulation Parameter Container
        '''

        args.beds = simpy.Resource(self.env, 
                                   capacity=args.beds)
        
        
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
        self.env.process(self.arrivals_generator('stroke'))
        self.env.process(self.arrivals_generator('tia'))
        self.env.process(self.arrivals_generator('neuro'))
                
        # run
        self.env.run(until=results_collection_period+warm_up)
        
        
    def get_arrival_dist_sample(self):
        
        if self.patient_type == 'stroke':
            inter_arrival_time = self.args.arrival_dist_samples['stroke'].sample()
        elif self.patient_type == 'tia':
            inter_arrival_time = self.args.arrival_dist_samples['tia'].sample()
        else:
            inter_arrival_time = self.args.arrival_dist_samples['neuro'].sample()
        
        return inter_arrival_time
            
        
    def arrivals_generator(self, patient_type):
        self.args.init_sampling()
            
        while True:
                
                self.patient_type = patient_type
            
                if self.patient_type == 'stroke':
                    self.stroke_count += 1
                elif self.patient_type == 'tia':
                    self.tia_count += 1
                else:
                    self.neuro_count += 1    

                
                yield self.env.timeout(self.get_arrival_dist_sample())
                
                self.patient_count += 1

                trace(f'Patient № {self.patient_count} ({patient_type}) arrives at: {self.env.now:.3f}')
                
                # create a new patient and pass in env and args
                new_patient = Patient(self.patient_count, patient_type, self.env, self.args)                

                # init the minor injury process for this patient
                self.env.process(new_patient.treatment())                 
            
                # keep a record of the patient for results calculation
                self.patients.append(new_patient)                
                
                
                
    def run_summary_frame(self):
        
        '''
        Utility function for final metrics calculation.
        
        Returns df containining
        total pts count
        count of each of pts types
        bed utilisation
        mean waiting time of bottom 90% of pts
        % of pts admitted in <4 hours
        '''
        # create nparray of all queue times, convert to hours
        patients_queue_times = np.array([patient.queue_time * 24 for patient in self.patients])
        
        #sort array in descending order, drops top 10% of values, calculate the mean 
        queue_bottom90 = np.mean(np.sort(patients_queue_times)[len(self.patients) // 10:])
        
        
        # calculate proportion of patient with queue time less than 4 hrs
        percent_4_less = (sum(patients_queue_times <= 4)/len(self.patients))*100
    
        #bed utilisation = sum(call durations) / (run length X no. BEDS)
        util = np.array([patient.treat_time 
                     for patient in self.patients]).sum() / (RUN_LENGTH * self.args.beds.capacity)
        
        average_treat_time = np.array([patient.treat_time 
                     for patient in self.patients]).sum() / self.patient_count
        

        df = pd.DataFrame({'1':{'1b Stroke Patient Arrivals':self.stroke_count,
                                '2 Bottom 90% Mean Treatment Waiting Time (hrs)': queue_bottom90, 
                                '4 Bed Utilisation (%)': util*100,
                                '1a Total Patient Arrivals':self.patient_count,
                                '1d Neuro Patient Arrivals':self.neuro_count,
                                '1c TIA Patient Arrivals':self.tia_count,
                                '5 Mean Total Time in Unit per patient(hrs)':average_treat_time,
                                '3 Patients Admitted to Unit within 4 hrs of arrival(%)': percent_4_less}})
        
        
        df = df.T
        df.index.name = 'rep'
        return df


# Functions for single and multiple runs

def single_run(scenario, 
               rc_period = RUN_LENGTH, 
               warm_up = 0,
               random_no_set = DEFAULT_RNG_SET):
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
    if random_no_set is not None:
        scenario.set_random_no_set(random_no_set)
    
    # create the model
    model = ASU(scenario)

    model.run(results_collection_period = rc_period, warm_up = warm_up)
    
    # run the model
    results_summary= model.run_summary_frame()
    
    return results_summary


def multiple_replications(scenario, 
                          rc_period=RUN_LENGTH,
                          warm_up=0,
                          n_reps=DEFAULT_N_REPS, 
                          n_jobs=-1,
                          random_no_set = DEFAULT_RNG_SET):
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
        
    random_no_set: int or None, optional (default=1)
        Controls the set of random seeds used by the stochastic parts of the 
        model.  Set to different ints to get different results.  Set to None
        for a random set of seeds.
        
    Returns:
    --------
    List
    '''    

    if random_no_set is not None:
        rng_sets = [random_no_set + rep for rep in range(n_reps)]
    else:
        rng_sets = [None] * n_reps
        
    res = Parallel(n_jobs=n_jobs)(delayed(single_run)(scenario, 
                                                      rc_period, 
                                                      warm_up, 
                                                      random_no_set=rng_set) 
                                    for rng_set in rng_sets)
    

    # format and return results in a dataframe
    df_results = pd.concat(res)
    df_results.index = np.arange(1, len(df_results)+1)
    df_results.index.name = 'rep'
    return df_results


