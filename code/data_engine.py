import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    data_dir = os.path.join(root_dir, "data")
    
    analysis_path = os.path.join(data_dir, "stock_performance.csv")
    sector_path = os.path.join(data_dir, "sector_mapping.csv")
    
    analysis_df = pd.read_csv(analysis_path)
    analysis_df['date'] = pd.to_datetime(analysis_df['date'])
    
    sector_df = pd.read_csv(sector_path)
    
    return analysis_df, sector_df