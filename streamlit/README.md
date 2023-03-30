# ASU-simpy
This file contains code for the simulation model for hpdm097 assignment 2



## Environment:

These simulation use the conda environment `deploy_st` included in `environment.yml` and the simulation code included in `asu_sim_streamlit.py`.



## User Manual

### Bulid and activate conda environment

```
# Create a new conda environment with the name "deploy_st" and install all the required packages listed in the environment.yml file.
conda env create --file binder/environment.yml

# Once the environment is created, activate it by running the following command
conda activate deploy_st
```

### See the interactive simulation model
1) Open a terminal or ssh into your Linux server 
2) Move working directory to file `streamlit` 
```
# Obtain the link to the simulation by running the following command
streamlit run asu_sim_streamlit.py
```

3) Open another terminal and enter the command below
```
ssh -i [pem_name].pem -CNL localhost:[provided_on_link]:localhost:[provided_on_link] ubuntu@XX.XXX.X.XXX
```
4) Copy the simulation link into your local browser to view



## Assessment Simulation

The period of interest for each simulation run is 1 year

### Primary (essential) research questions

Parameters:

The default interarrival time and length of stay in the model are suitable for primary (essential) research questions


Results:

11 beds are needed for 90% of patients being admitted to the stroke unit within 4 hours of their arrival at the hospital and maintain a bed utilisation in excess of 70%.


### Secondary (desirable) research questions

Parameters:

For the secondary (desirable) research questions, the interarrival time for each type of patients are 10% shortened to simulate 10% increase in patients requiring an admission. Please change the time as follows:

| Patient Type                     | Mean IAT (days) |
|----------------------------------|-----------------|
| Acute strokes                    | 1.08            |
| Transient Ischaemic Attack (TIA) | 8.55            |
| Complex Neurological             | 3.15            |

Results:

The percentage of patients admitted to the stroke unit within 4 hours of arrival is decreased while the bed utility increased.

13 beds are needed for 90% of patients being admitted to the stroke unit within 4 hours of their arrival at the hospital and maintain a bed utilisation in excess of 70%.



## Results table

|                                                     | 9 beds (present) | 11 beds (present) | 9 beds (2030) | 13 beds (2030) |
|-----------------------------------------------------|------------------|-------------------|---------------|----------------|
|Total Patient Arrivals	                              | 454.20           | 454.20            | 501.20        | 501.20         |
|Stroke Patient Arrivals	                        | 315.60           | 315.60            | 347.80        | 347.80         |
|TIA Patient Arrivals	                              | 36.00            | 36.00             | 41.40         | 41.40          |
|Neuro Patient Arrivals	                              | 102.60           | 102.60            | 112.00        | 112.00         |
|Bottom 90% Mean Treatment Waiting Time (hrs)	      | 8.57             | 0.34              | 27.35         | 0.22           |
|Patients Admitted to Unit within 4 hrs of arrival(%) | 72.01            | 91.24             | 54.63         | 94.15          |
|Bed Utilisation (%)	                              | 76.29            | 77.07             | 83.52         | 85.03          |
|Mean Total Time in Unit per patient(hrs)	            | 5.52             | 5.57              | 5.47          | 5.57           |


## Reference
```
@software{monks_thomas_2022_6772475,
  author       = {Monks, Thomas and
                  Harper, Alison and
                  Taylor, J.E, Simon and
                  Anagnostou, Anastasia},
  title        = {TomMonks/treatment-centre-sim: v0.4.0},
  month        = jun,
  year         = 2022,
  publisher    = {Zenodo},
  version      = {v0.4.0},
  doi          = {10.5281/zenodo.6772475},
  url          = {https://doi.org/10.5281/zenodo.6772475}
}
```
