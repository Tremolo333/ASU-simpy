# ASU-simpy
The depo contains random code for the final hpdm097 assignment
      
V4.0 contains a basic working ASU model as specified in assignment      
V4.1 added utility function to calculate final results, fixed the problem with the first three patients starting their treatment at 00:00. Each patient now yields a proper timeout       
V4.2 added bed utilisation       
       
V4.3 final results are now calculated by a function within ASU class. there is now a separate function for a single model run that returns a df with results (tbc with multiple runs)

## TO DO:

1) (Timur) Implement high quality output analysis techniques (WS6). Take into account the amount of time required for the ASU to reach "plateau" - stable in/outflow of patients, adjust the run length.

2) Wrap the model into the streamlit, add various sliders, run button, whatever else (make it look neat and professional)      
                                                                                                                                         
      Link to streamlit github repo: https://github.com/health-data-science-OR/streamlit_tutorial    <<woking on this(inni)
                                                                                                                                         
3) Run the model with all means of IAT distributions decreased by 10%, monitor the stroke patients to answer the secondary question (he percentage of patients admitted to the stoke unit within 4 hours of arrival, bed occupancy and if more bed capacity is needed. )

4) Bring the code to PEP8 standarts, check if it can be simplified.

5) Produce an exceptional lab report no less than 900 words (<1000), use ChatGPT to help.

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

## Assessment Simulation Parameter

### Part 1

(TBC)

### Part 2

(TBC)

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
