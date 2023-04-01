# ASU-simpy
The depo contains random code for the final hpdm097 assignment
      
V4.0 contains a basic working ASU model as specified in assignment      
V4.1 added utility function to calculate final results, fixed the problem with the first three patients starting their treatment at 00:00. Each patient now yields a proper timeout       
V4.2 added bed utilisation         
V4.3 final results are now calculated by a function within ASU class. there is now a separate function for a single model run that returns a df with results       
V4.4 implemented multiple run function, seed sets generation for reproducible runs    
V4.5 added more parameters to the summary frame     
V5.0 simplified the code significantly by storing samples from iat and treatment distributions in 2 separate dictionaries, rather than a separate value for every patient type. type1/type2/type3 replaced with 'stroke'/'tia'/'neuro throughout. there is now single arrival generator function and single treatment function. arrival generator now takes patient type as a parameter that defines future pathway. simplified the summary frame function              
V5.1 there are now separate functions to get samples outside of treatment() and arrivals_generator()

V5.2 implemented controllable/uncontrollable sampling, updated streamlit file and source code. error fixed with bed utilisation calculation as the formula was incorrect, n_beds wasn't referred to properly within a class               

## TO DO:

from the workshop №6, in a separate file perform the following and modify the source code        
1) Calculate model warm-up period and take it into account - the amount of time required for the ASU to reach "plateau" - stable in/outflow of patients.     

2) Select the number of replications to run to obtain reliable results.        

3) Present the results.          

4) Bring the code to PEP8 standarts, check if it can be simplified.          


      
      Lab report link: https://docs.google.com/document/d/1u7SbKhrViICDEj4Ie1E0ig8s308FIrtA9Nh5W-4v-yQ/edit?usp=sharing         
      Link to streamlit github repo: https://github.com/health-data-science-OR/streamlit_tutorial        
