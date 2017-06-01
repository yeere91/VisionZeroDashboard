import numpy as np
import pandas as pd
import datetime
import urllib

def get_data():
  raw_data = pd.DataFrame()
  offset = 0
  limit = 1000

  query =  ("https://data.cityofnewyork.us/resource/qiz3-axqb.json?" + 
            "$where=borough=%22BROOKLYN%22" +
            "&$order=date%20DESC" +
            "&$limit=" + str(limit) + 
            "&$offset=" + str(offset))
  print pd.read_json(query)

  ## Drop location column
  ##raw_data = raw_data.drop('location', axis=1)