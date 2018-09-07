# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from IPython.display import display
import pandas as pd
import sys
sys.path.append("T:/BCB/")
import BISdbConfig as config

# pybis needs environment variables to connect to the database.
#import os
#os.environ['DB_USERNAME']=config.user
#os.environ['DB_PASSWORD']=config.password
#os.environ['MONGODB_SERVER']="54.91.95.139"
#os.environ['DB_DATABASE']="bis"
from pybis import db





bisDB = db.Db.connect_mongodb("bis")
esaWPSpecies = bisDB["FWS_Work_Plan_Species"]
print(esaWPSpecies)