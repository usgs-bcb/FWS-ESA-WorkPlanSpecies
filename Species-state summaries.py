# -*- coding: utf-8 -*-
"""
nmtarr 9/7/2018

Description: Script used in developing State range summaries.ipynb.

"""
#from IPython.display import display as display1
import us
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 12)
pd.set_option('display.max_rows', 100)
# Widens the display in a notebook
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

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

# Connect to bis and get collection
from pybis import db
bisDB = db.Db.connect_mongodb("bis")
esaWPSpecies = bisDB["FWS_Work_Plan_Species"]


## Get a list of species names to loop on.
spp = [record["Submitted Data"]["Scientific Name"] for record in esaWPSpecies.find()]

for sp in spp[:3]:
    # Build dataframe to fill out
    columns=[]
    df0 = pd.DataFrame(index=[str(x) for x in us.STATES], columns=columns)
    df0.index.name="State"
    df0.name=sp
    
    ##########################################################################  FWS
    # Fill out ECOS column with whether or not the ECOS account lists the state
    try:
        Synth = esaWPSpecies.find_one({"Submitted Data.Scientific Name": sp})['Synthesis']
        FWS_states = Synth['FWS Range List']
        for x in FWS_states:
            state_name = x.strip()
            df0.loc[state_name, 'FWS_range(y/n)'] = 1
    except:
        print("Exception -- FWS range")
        
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
        print("Exception -- BISON state list")
    
    #########################################################################  SGCN 
    # Which states declared it SGCN?
    try:
        for x in Synth['SGCN State List 2005']:
            df0.loc[x, 'SGCN_2005(y/n)'] = 1
    
    except:
        print("Exception -- SGCN 2005") 
        
    try:
        for x in Synth['SGCN State List 2015']:
            df0.loc[x, 'SGCN_2015(y/n)'] = 1    
    except:
        print('Exception -- SGCN 2015')
                
    ###################################################################  GAP habitat 
    # Which states have potential habitat (GAP)?
    try:
        GAP_states = Synth['States with GAP Species Potential Habitat']
        for x in GAP_states:
            state_name = x.strip()
            df0.loc[state_name, 'has_GAP_habitat(y/n)'] = 1
    except:
        print('Exception -- GAP states, species.')
    
    #################################################################  Clean up\
    df1 = df0.fillna(0).astype(int)
    # get rid of non-CONUS states
    lowers = [str(x) for x in us.STATES_CONTINENTAL]
    print(sp + ' state range summary')
    df2 = df1.filter(items=lowers, axis=0)
    print(df2)
    print('\n\n')
    