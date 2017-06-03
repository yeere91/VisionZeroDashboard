import numpy as np
import pandas as pd
import datetime
import urllib
import sqlite3
import sqlalchemy

raw_data = pd.DataFrame()
offset = 0
limit = 50000

query =  ("https://data.cityofnewyork.us/resource/qiz3-axqb.json?" + 
          "$where=borough=%22BROOKLYN%22" +
          "&$order=date%20DESC" +
          "&$limit=" + str(limit) + 
          "&$offset=" + str(offset))

while(not pd.read_json(query).empty):
    data = pd.read_json(query)
    print("Obtaining Data from ") + str(offset) + " to " + str(offset + limit)
    raw_data = raw_data.append(data)
    offset = offset + 50000
    query =  ("https://data.cityofnewyork.us/resource/qiz3-axqb.json?" + 
              "$where=borough=%22BROOKLYN%22" +
              "&$order=date%20DESC" +
              "&$limit=" + str(limit) + 
              "&$offset=" + str(offset))

## Drop location column
raw_data = raw_data.drop('location', axis=1)

engine = sqlalchemy.create_engine('postgres://tmfykgvqcxxiiy:b35d2c8219898eb3558d41f5f335142f55f74a39404edc57fc6b3c7061da843f@ec2-23-21-169-238.compute-1.amazonaws.com:5432/d64fq3p9ro085j', client_encoding='utf8')
conn = engine.raw_connection()
## Push the dataframe into the collisions table.
raw_data.to_sql("collisions", engine, flavor='postgresql')