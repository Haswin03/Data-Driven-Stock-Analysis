import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    data_dir = os.path.join(current_dir, "data")
    
    analysis_path = os.path.join(data_dir, "stock_performance.csv")
    sector_path = os.path.join(data_dir, "sector_mapping.csv")
    
    analysis_df = pd.read_csv(analysis_path)
    if 'date' in analysis_df.columns:
        analysis_df['date'] = pd.to_datetime(analysis_df['date'])
        
    sector_df = pd.read_csv(sector_path)
    
    return analysis_df, sector_df