import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from data_engine import load_data

# ---------------------------------------------------------
# 1. Page Configuration (Must be the first Streamlit command)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nifty 50 Performance Dashboard", 
    page_icon="📈", 
    layout="wide"
)

# ---------------------------------------------------------
# 2. Load Data (Cached via data_engine.py)
# ---------------------------------------------------------
# Assuming load_data() handles the DB connection and initial cleaning
try:
    analysis_df, sector_df = load_data()
except Exception as e:
    st.error(f"Failed to connect to the database or load data. Error: {e}")
    st.stop()

# ---------------------------------------------------------
# 3. Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Nifty_50_Logo.svg/1200px-Nifty_50_Logo.svg.png", width=150)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Market Overview", 
    "Volatility & Trends", 
    "Sectors & Correlation", 
    "Monthly Deep Dive"
])

st.sidebar.markdown("---")
st.sidebar.info("Dashboard analyzing the performance of Nifty 50 stocks over the past year.")

# ---------------------------------------------------------
# 4. Page Routing & Logic
# ---------------------------------------------------------

if page == "Market Overview":
    st.title("Nifty 50 Market Overview")
    
    # Calculate Key Metrics
    perf = analysis_df.groupby('Ticker').agg(
        First_Price=('open', 'first'),
        Last_Price=('close', 'last')
    ).reset_index()
    perf['Yearly_Return_%'] = ((perf['Last_Price'] - perf['First_Price']) / perf['First_Price']) * 100
    
    total_green = len(perf[perf['Yearly_Return_%'] > 0])
    total_red = len(perf[perf['Yearly_Return_%'] < 0])
    avg_price = analysis_df.groupby('Ticker')['close'].last().mean()
    avg_volume = analysis_df['volume'].mean()

    # Display Top-Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Green Stocks (Gains)", total_green)
    col2.metric("Red Stocks (Losses)", total_red)
    col3.metric("Avg Stock Price", f"₹{avg_price:,.2f}")
    col4.metric("Avg Daily Volume", f"{avg_volume:,.0f}")
    
    st.markdown("---")
    
    # Display Top 10 DataFrames
    col_green, col_red = st.columns(2)
    
    with col_green:
        st.subheader("🟢 Top 10 Green Stocks")
        top_10_green = perf.nlargest(10, 'Yearly_Return_%')[['Ticker', 'Yearly_Return_%']]
        # Formatting for display
        top_10_green['Yearly_Return_%'] = top_10_green['Yearly_Return_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(top_10_green, hide_index=True, use_container_width=True)
        
    with col_red:
        st.subheader("🔴 Top 10 Loss Stocks")
        top_10_red = perf.nsmallest(10, 'Yearly_Return_%')[['Ticker', 'Yearly_Return_%']]
        # Formatting for display
        top_10_red['Yearly_Return_%'] = top_10_red['Yearly_Return_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(top_10_red, hide_index=True, use_container_width=True)


elif page == "Volatility & Trends":
    st.title("Volatility & Cumulative Trends")
    
    # --- Volatility Chart ---
    st.subheader("Top 10 Most Volatile Stocks")
    vol_df = analysis_df.groupby('Ticker')['daily_return'].std().reset_index()
    vol_df.columns = ['Ticker', 'Volatility']
    top_10_volatile = vol_df.nlargest(10, 'Volatility')

    fig_vol, ax_vol = plt.subplots(figsize=(12, 5))
    sns.barplot(
        x='Ticker', y='Volatility', data=top_10_volatile, 
        palette='magma', hue='Ticker', legend=False, ax=ax_vol
    )
    ax_vol.set_xlabel('Stock Ticker', fontsize=10)
    ax_vol.set_ylabel('Volatility (Std Dev)', fontsize=10)
    ax_vol.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig_vol)
    
    st.markdown("---")
    
    # --- Cumulative Returns Chart ---
    st.subheader("Cumulative Return of Top 5 Performers")
    analysis_df['daily_return_clean'] = analysis_df['daily_return'].fillna(0)
    analysis_df['cum_return'] = analysis_df.groupby('Ticker')['daily_return_clean'].transform(lambda x: (1 + x).cumprod() - 1)

    final_returns = analysis_df.groupby('Ticker')['cum_return'].last().reset_index()
    top_5_tickers = final_returns.nlargest(5, 'cum_return')['Ticker'].tolist()
    top_5_df = analysis_df[analysis_df['Ticker'].isin(top_5_tickers)]

    fig_cum, ax_cum = plt.subplots(figsize=(12, 5))
    for ticker in top_5_tickers:
        subset = top_5_df[top_5_df['Ticker'] == ticker]
        ax_cum.plot(subset['date'], subset['cum_return'], label=ticker, linewidth=2)

    ax_cum.set_xlabel('Date', fontsize=10)
    ax_cum.set_ylabel('Cumulative Return', fontsize=10)
    ax_cum.legend(title='Stock Ticker')
    ax_cum.grid(True, which='both', linestyle='--', alpha=0.5)
    ax_cum.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    st.pyplot(fig_cum)


elif page == "Sectors & Correlation":
    st.title("Sectors & Correlation")
    
    # Needs the perf dataframe again
    perf = analysis_df.groupby('Ticker').agg(
        First_Price=('open', 'first'),
        Last_Price=('close', 'last')
    ).reset_index()
    perf['Yearly_Return_%'] = ((perf['Last_Price'] - perf['First_Price']) / perf['First_Price']) * 100
    
    # --- Sector Performance ---
    st.subheader("Average Yearly Return by Sector")
    sector_merge = pd.merge(perf, sector_df, left_on='Ticker', right_on='Ticker_Clean')
    sector_avg_return = sector_merge.groupby('sector')['Yearly_Return_%'].mean().reset_index()
    sector_avg_return = sector_avg_return.sort_values('Yearly_Return_%', ascending=False)

    fig_sec, ax_sec = plt.subplots(figsize=(12, 5))
    sns.barplot(
        x='sector', y='Yearly_Return_%', data=sector_avg_return, 
        palette='coolwarm', hue='sector', legend=False, ax=ax_sec
    )
    ax_sec.set_xlabel('Industry Sector', fontsize=10)
    ax_sec.set_ylabel('Average Yearly Return (%)', fontsize=10)
    plt.xticks(rotation=45, ha='right')
    ax_sec.grid(axis='y', linestyle='--', alpha=0.5)
    
    for index, row in enumerate(sector_avg_return['Yearly_Return_%']):
        y_pos = row + 1 if row > 0 else row - 2
        ax_sec.text(index, y_pos, f"{row:.1f}%", color='black', ha="center", fontsize=9)
    st.pyplot(fig_sec)
    
    st.markdown("---")
    
    # --- Correlation Heatmap ---
    st.subheader("Stock Price Correlation Heatmap")
    pivot_df = analysis_df.pivot_table(index='date', columns='Ticker', values='daily_return')
    corr_matrix = pivot_df.corr()

    fig_corr, ax_corr = plt.subplots(figsize=(14, 12))
    sns.heatmap(
        corr_matrix, annot=False, cmap='YlOrBr', 
        linewidths=0.5, square=True, ax=ax_corr
    )
    ax_corr.set_xlabel('')
    ax_corr.set_ylabel('')
    st.pyplot(fig_corr)


elif page == "Monthly Deep Dive":
    st.title("Monthly Gainers & Losers")
    
    # Data Preparation
    analysis_df['month_yr'] = analysis_df['date'].dt.to_period('M').astype(str)
    monthly_perf = analysis_df.groupby(['Ticker', 'month_yr']).agg(
        start_price=('open', 'first'),
        end_price=('close', 'last')
    ).reset_index()
    monthly_perf['monthly_return'] = ((monthly_perf['end_price'] - monthly_perf['start_price']) / monthly_perf['start_price']) * 100

    unique_months = sorted(monthly_perf['month_yr'].unique())
    
    # Interactive Streamlit Widget
    selected_month = st.selectbox("Select a Month to Analyze:", unique_months)
    
    month_data = monthly_perf[monthly_perf['month_yr'] == selected_month]
    top_5_gainers = month_data.nlargest(5, 'monthly_return')
    top_5_losers = month_data.nsmallest(5, 'monthly_return')
    
    # Plot side-by-side using Streamlit columns
    fig_month, (ax_gain, ax_loss) = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.barplot(x='monthly_return', y='Ticker', data=top_5_gainers, ax=ax_gain, palette='Greens_r', hue='Ticker', legend=False)
    ax_gain.set_title(f'Top 5 Gainers: {selected_month}', fontsize=12, fontweight='bold')
    ax_gain.set_xlabel('Monthly Return (%)')
    ax_gain.set_ylabel('')
    
    sns.barplot(x='monthly_return', y='Ticker', data=top_5_losers, ax=ax_loss, palette='Reds_r', hue='Ticker', legend=False)
    ax_loss.set_title(f'Top 5 Losers: {selected_month}', fontsize=12, fontweight='bold')
    ax_loss.set_xlabel('Monthly Return (%)')
    ax_loss.set_ylabel('')
    
    plt.tight_layout()
    st.pyplot(fig_month)