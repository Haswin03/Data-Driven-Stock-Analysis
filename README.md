# 📈 Nifty 50 Stock Performance Dashboard

[![Nifty50 Stock Analysis Streamlit App](https://static.streamlit.io/badges/streamlit_badge.svg)](https://data-driven-stock-analysis-demo.streamlit.app/)

## 📝 Project Overview
The **Stock Performance Dashboard** is a comprehensive financial analytics project designed to visualize and analyze the performance of India's top 50 blue-chip companies (Nifty 50) over the past year. 

This project bridges the gap between raw data and actionable financial insights. By extracting deeply nested daily trading data (Open, Close, High, Low, Volume) and transforming it into interactive visual dashboards, this solution helps investors, financial analysts, and market enthusiasts track trends, assess risk, and make data-driven decisions.

The project was executed in two distinct phases:
* **Phase 1:** Data Engineering, Python Analytics, and Interactive Web Deployment using **Streamlit**.
* **Phase 2:** Advanced Business Intelligence and Data Modeling using **Power BI**.

---

## 🛠️ Technology Stack
* **Language:** Python (3.12+)
* **Data Manipulation:** Pandas, NumPy
* **Database:** MySQL / PostgreSQL / SQLAlchemy
* **Data Visualization:** Matplotlib, Seaborn, Streamlit
* **Business Intelligence:** Microsoft Power BI (DAX, Data Modeling)
* **Version Control:** Git & GitHub

---

## 🏗️ Architecture & Approach

### 1. Data Extraction & Transformation (ETL)
The raw data was initially provided in a complex, nested folder structure containing `YAML` files organized by month and date.
* **Extraction:** Built Python scripts to parse the directory tree and extract the daily trading metrics.
* **Transformation:** Restructured the nested YAML data into flat, structured formats, ultimately generating 50 independent `.csv` files (one for each stock ticker) to allow for isolated symbol analysis and database injection.

### 2. Database Integration
Cleaned data was ingested into a SQL relational database using `SQLAlchemy`, ensuring data validation, integrity, and optimized querying capabilities for large datasets.

---

## 📊 Analytical Features & Visualizations

The core of the project relies on five primary analytical pillars, deployed across both Streamlit and Power BI:

### 1. Market Summary & Core Metrics
* **Top 10 Green & Red Stocks:** Sorted and visualized the best and worst performers based on annual percentage return.
* **Market Breadth:** Calculated the overall ratio of advancing (green) vs. declining (red) stocks.
* **Volume & Price:** Computed average trading volumes and prices across the entire index to gauge market liquidity.

### 2. Volatility Analysis (Risk Assessment)
* **Objective:** Measure price fluctuation and investment risk.
* **Metric:** Calculated the standard deviation of daily returns: `(Close - Prev Close) / Prev Close`.
* **Visualization:** Bar charts highlighting the Top 10 Most Volatile Stocks, allowing investors to identify high-risk assets.

### 3. Cumulative Return Over Time
* **Objective:** Track the compound growth of assets over the calendar year.
* **Metric:** Applied a running total (cumulative product) of daily returns.
* **Visualization:** Multi-line charts displaying the growth trajectories of the top 5 performing stocks, providing a clear comparison of sustained momentum.

### 4. Sector-Wise Performance
* **Objective:** Gauge broader macroeconomic trends and industry sentiment.
* **Metric:** Merged stock data with a separate Sector Mapping dataset to group tickers by industry (e.g., IT, Financials, Energy). Calculated the average annual return per sector.
* **Visualization:** Sector bar charts to instantly highlight which industries are driving the market forward and which are lagging.

### 5. Stock Price Correlation (Diversification Strategy)
* **Objective:** Understand how different stocks move in tandem to aid in portfolio diversification.
* **Metric:** Computed the Pearson correlation coefficient between the daily closing returns of all 50 stocks.
* **Visualization:** A dense, color-coded **Correlation Heatmap**. 
    * *Green/Blue:* Stocks move together. 
    * *Red:* Stocks move inversely.
    * *(Note: Implemented using native matrix cross-filtering and DAX statistical variance models in Power BI).*

### 6. Granular Monthly Trends
* **Objective:** Identify short-term momentum shifts.
* **Metric:** Grouped data by month to calculate monthly percentage changes.
* **Visualization:** A grid of 12 charts showcasing the Top 5 Gainers and Losers for every single month of the year.

---

## 🚀 Deployment & Results

### Phase 1: Streamlit Application
A fully interactive, Python-based web application. Users can interact with the data in real-time, filter by specific stocks, and generate instant visual reports using Pandas and Matplotlib/Seaborn.

### Phase 2: Power BI Dashboard
A professional-grade Business Intelligence suite. This phase involved creating a robust Star Schema data model, writing complex DAX measures (for dynamic Volatility, Averages, and Pearson Correlation calculations without syntax limitations), and designing an intuitive, executive-ready graphical interface.

---

## 🏗️ Project Architecture

The project has been optimized for seamless cloud deployment, decoupling the local PostgreSQL database requirement in favor of a robust flat-file CSV architecture.

```text
📁 EDA PROJECT/
│
├── 📄 app.py                   # Main Streamlit application script (UI and Logic)
├── 📄 data_engine.py           # Data loader module (Bridges UI with CSV assets)
├── 📄 requirements.txt         # Python dependencies optimized for cloud binary builds
├── 📄 packages.txt             # System-level dependencies (e.g., libz-dev) for cloud hosting
├── ⚙️ .gitignore               # Git rules protecting the repo from heavy raw data/Power BI files
│
├── 📁 data/                    # Cleaned, production-ready datasets
│   ├── 📊 stock_performance.csv  # Core historical daily stock data
│   └── 📊 sector_mapping.csv     # Ticker-to-sector categorical mappings
│
├── 📁 code/                    # Development workspace
│   └── 📓 project_02.ipynb       # Original Jupyter Notebook for ETL and testing
│
└── 📁 Power BI files/          # (Local Only) Supplementary Power BI dashboard files
