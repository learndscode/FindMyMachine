import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import reverse_geocoder as rg
import pycountry

def get_location(lat, lon):
  try:
      result = rg.search((lat, lon), mode=1)[0]
      return pd.Series([result['name'], result['admin1'], result['cc']])
  except Exception:
      return pd.Series([None, None, None])
  
def get_country_name(code):
    country = pycountry.countries.get(alpha_2=code)
    return country.name if country else code