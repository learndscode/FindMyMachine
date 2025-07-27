import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import reverse_geocoder as rg
import pycountry

def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code

def get_location(lat, lon):
  try:
      result = rg.search((lat, lon), mode=1)[0]
      return pd.Series([result['name'], result['admin1'], get_country_name(result['cc'])])
  except Exception:
      return pd.Series([None, None, None])
  
def review_needed(row):
    if row['Expected Country'] == row['Country']:
       if row['Expected State'] == row['State']:
          return 'No'
       else:
          return 'Yes'
    else : 
       return 'Yes'
    
# Function to style individual cells    
def highlight_cells(row):
    styles = [''] * len(row)
    if row['Expected Country'] != row['Country']:
        styles[row.index.get_loc('Expected Country')] = 'background-color: #FFC7CD; color: darkred'
        styles[row.index.get_loc('Country')] = 'background-color: #FFC7CD; color: darkred'
    if row['Expected State'] != row['State']:
        styles[row.index.get_loc('Expected State')] = 'background-color: lemonchiffon'
        styles[row.index.get_loc('State')] = 'background-color: lemonchiffon'
    if row['Needs Review'] == 'Yes':
        styles[row.index.get_loc('Needs Review')] = 'background-color: #FFC7CD; color: darkred'

    return styles
