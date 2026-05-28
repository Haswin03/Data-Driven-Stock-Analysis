import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_dir = os.path.dirname(current_dir)
    
    data_dir = os.path.join(root_dir, "data")
    
    analysis_path = os.path.join(data_dir, "stock_performance.csv")
    sector_path = os.path.join(data_dir, "sector_mapping.csv")
    
    if not os.path.exists(analysis_path):
        raise FileNotFoundError(f"Missing file: {analysis_path}. Ensure it is inside the 'data' folder.")
    if not os.path.exists(sector_path):
        raise FileNotFoundError(f"Missing file: {sector_path}. Ensure it is inside the 'data' folder.")
        
    analysis_df = pd.read_csv(analysis_path)
    sector_df = pd.read_csv(sector_path)
    
    if 'date' in analysis_df.columns:
        analysis_df['date'] = pd.to_datetime(analysis_df['date'])
        
    return analysis_df, sector_df