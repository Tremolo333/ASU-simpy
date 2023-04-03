# ASU-simpy

This project was done by 720090075 Tymur Terletskyi and 720079703 Inni Choi.

There are two ways to run the model:               
№1: Create environment from the binder folder, run jupyter notebook V6.6 (which also contains the lab report).             
№2: Create environment from the binder folder, follow instructions in the readme file from streamlit folder.          
Set seed value to 333 to reproduce results in both cases.             




The obtained results are also duplicated as screenshots of two tables (one deriverd from default parameters, another from all IAT decreased by 10%) and two plots (one justifiyng the warm-up period of 250 selection, another - the assessed number of runs required to obtain valid results).          

Changelog:         
      
V4.0 contains a basic working ASU model as specified in assignment      
V4.1 added utility function to calculate final results, fixed the problem with the first three patients starting their treatment at 00:00. Each patient now yields a proper timeout       
V4.2 added bed utilisation         
V4.3 final results are now calculated by a function within ASU class. there is now a separate function for a single model run that returns a df with results       
V4.4 implemented multiple run function, seed sets generation for reproducible runs    
V4.5 added more parameters to the summary frame     
V5.0 simplified the code significantly by storing samples from iat and treatment distributions in 2 separate dictionaries, rather than a separate value for every patient type. type1/type2/type3 replaced with 'stroke'/'tia'/'neuro throughout. there is now single arrival generator function and single treatment function. arrival generator now takes patient type as a parameter that defines future pathway. simplified the summary frame function              
V5.1 there are now separate functions to get samples outside of treatment() and arrivals_generator()                   
V5.2 implemented controllable/uncontrollable sampling, updated streamlit file and source code. added the checkbox. error fixed with bed utilisation calculation as the formula was incorrect, n_beds wasn't referred to properly within a class. fixed pts admitted within 4 hours calculation       
V6.0 added warm-up auditor       
V6.1 calculated warm-up period, all metrics are now calculated only after the warm-up          
V6.2 estimated number of replications needed to achive 0.05 p-value for final results, but only for 2 basic metrics - mean bed waiting time and bed utilisation      
V6.3 warm_up parameter passed to scenario class, now it's taken into account properly. proper metrics calculation                         
V6.4 bottom 90% waiting time wasn't calculating properly, now fine       
V6.5 cleared up the code          
V6.6 included the lab report          
