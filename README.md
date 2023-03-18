# ASU-simpy
The depo contains random code for the final hpdm097 assignment
      
V3.0 contains working version of patients inter-arrival times generator. there are three generators working simultaneously, each for each type of patients. the most common admitted type is Stroke (which makes sence as it has the shortest IAT), there is a total of 451 entries (which makes sence if you count how many patients there would have been manually, ignoring the distributions. should be around 442), mean queue time 1.91 days (which also makes sence and means that there is room for improvement)

V4.0 contains an ASU model and the answer to the first question (bed capacity needed to achieve an annual target of 90% of patients being admitted to the stroke unit within 4 hours of their arrival at the hospital)

TO DO:
1) Calculate bed utilisation for the second question ( The managers would also like to know if they can achieve 90% performance and maintain a bed utilisation in excess of 70%)
2) Run the model with all means of IAT distributions increased by 10%, monitor the stroke patients to answer the secondary question (he percentage of patients admitted to the stoke unit within 4 hours of arrival, bed occupancy and if more bed capacity is needed. )
3) Implement high quality output analysis techniques (WS6).
4) Wrap the model into a streamlit, add various sliders, run button, whatever else (make it look neat and professional)
5) Produce an exceptional lab report no less than 900 words (<1000), use ChatGPT to help.
