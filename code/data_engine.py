# data_engine.py
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

@st.cache_data
def load_data():
    # Connect to PostgreSQL
    engine = create_engine('postgresql://postgres:TARS@localhost:5432/nifty50_db')
    
    # Query the main data
    query = 'SELECT "Ticker", "date", "close", "open", "volume" FROM stock_performance'
    analysis_df = pd.read_sql(query, engine)
    
    # Query the sector mapping
    sector_query = 'SELECT * FROM sector_mapping'
    sector_df = pd.read_sql(sector_query, engine)
    
    # Apply global data cleansing & sorting
    analysis_df['date'] = pd.to_datetime(analysis_df['date'])
    analysis_df = analysis_df.sort_values(['Ticker', 'date']).reset_index(drop=True)
    analysis_df['daily_return'] = analysis_df.groupby('Ticker')['close'].pct_change()
    
    return analysis_df, sector_df