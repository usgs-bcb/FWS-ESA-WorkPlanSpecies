# -*- coding: utf-8 -*-
"""
nmtarr 9/7/2018


"""
# import config file with username and password
import sys
sys.path.append("T:/BCB/")
import BISdbConfig as config

# pybis needs environment variables to connect to the database.
import os
os.environ['DB_USERNAME']=config.user
os.environ['DB_PASSWORD']=config.password
os.environ['MONGODB_SERVER']="54.91.95.139"
os.environ['DB_DATABASE']="bis"

from pybis import db
from IPython.display import display
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 12)
pd.set_option('display.max_rows', 100)
import us
import pprint

bisDB = db.Db.connect_mongodb("bis")
esaWPSpecies = bisDB["FWS_Work_Plan_Species"]


## Species names
#for record in esaWPSpecies.find({"Synthesis.Unique Scientific Names.1":{"$exists":True}}):
#    print ("Submitted Name:", record["Submitted Data"]["Scientific Name"])
#    try:
#        print ("ECOS Name:", record["ECOS Scrape"]["Scientific Name"])
#        print ("ECOS TSN:", record["ECOS Scrape"]["TSN"])
#    except:
#        pass
#    try:
#        print ("TESS Name:", record["TESS"]["SCINAME"])
#    except:
#        pass
#    for itisRecord in record["ITIS"]:
#        print ("ITIS:", itisRecord["nameWInd"], itisRecord["usage"], itisRecord["tsn"])
#    print ("----------")
    
sp = "Ambystoma barbouri"


# Build dataframe to fill out
columns=[]
df0 = pd.DataFrame(index=[str(x) for x in us.STATES], columns=columns)
df0.index.name="State"

##########################################################################  FWS
# Fill out ECOS column with whether or not the ECOS account lists the state
try:
    Synth = esaWPSpecies.find_one({"Submitted Data.Scientific Name": sp})['Synthesis']
    FWS_states = Synth['FWS Range List']
    for x in FWS_states:
        state_name = x.strip()
        df0.loc[state_name, 'FWS_range(y/n)'] = 1
except:
    print("No FWS range")
    
########################################################################  BISON
# How many occurrences are in each state?
try:
    bison = esaWPSpecies.find_one({"Submitted Data.Scientific Name": sp})['BISON']
    bison_states = bison["US State Occurrences"]
    for state in bison_states:
        state_name = list(state.keys())[0]
        df0.loc[state_name, "BISON_occurrences"]=int(state[state_name])
except:
    print("No BISON records?")

# Which states have bison occurrences?
try:
    BISON_states = Synth['States with BISON Occurrence Data']
    for x in BISON_states:
        state_name = x.strip()
        df0.loc[state_name, 'Has_BISON_Data(y/n)'] = 1
except:
    print("ERROR getting bison state list")

#########################################################################  SGCN 
# Which states declared it SGCN?
try:
    SGCN = esaWPSpecies.find_one({"Submitted Data.Scientific Name": sp})['SGCN']
    for x in SGCN['State List Summary']:
        if list(x.keys())[0] == 2005:
            statess = x['2005']['States']
            for z in statess:
                df0.loc[z, 'SGCN_2005(y/n)'] = 1
        elif list(x.keys())[0] == 2015:
            statess = x['2015']['States']
            for z in statess:
                df0.loc[z, 'SGCN_2015(y/n)'] = 1  
except:
    print("No SGCN")   

print(df0)   

df0.to_csv("T:/temp/FWS-ESA_temp.csv")           
#            
###################################################################  GAP habitat 
##
#for record in esaWPSpecies.find({"GAP":{"$exists":True}}):
#    pprint.pprint(record)
#    
#    
#    
#try:
#    
#    GAP = esaWPSpecies.find_one({"GAP":{"$exists":True}},{"Submitted Data":1,"GAP":1})
#    
#except:
#    print("No GAP")
#    
#    
#    
    