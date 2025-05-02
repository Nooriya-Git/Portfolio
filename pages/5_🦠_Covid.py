# covid_analysis_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load COVID-19 dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# App title
st.title("🌍 COVID-19 Data Analysis Dashboard")
st.markdown("Interactive exploration of global COVID-19 data")

# Sidebar filters
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    'Select Countries',
    options=df['location'].unique(),
    default=['United States', 'India', 'Brazil', 'Germany', 'South Africa']
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[datetime(2020,3,1), df['date'].max().to_pydatetime()],
    min_value=df['date'].min().to_pydatetime(),
    max_value=df['date'].max().to_pydatetime()
)

# Process data
df_filtered = df[
    (df['location'].isin(selected_countries)) & 
    (df['date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# Main dashboard
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Analysis", "Comparisons"])

with tab1:
    st.header("Global Overview")
    
    # Worldwide totals
    total_cases = df.groupby('date')['total_cases'].max().ffill().iloc[-1]
    total_deaths = df.groupby('date')['total_deaths'].max().ffill().iloc[-1]
    
    col1, col2 = st.columns(2)
    col1.metric("Total Confirmed Cases", f"{total_cases:,.0f}")
    col2.metric("Total Reported Deaths", f"{total_deaths:,.0f}")
    
    # Worldwide trend
    st.subheader("Global Daily Cases Trend")
    global_daily = df.groupby('date').agg({'new_cases':'sum', 'new_deaths':'sum'}).reset_index()
    fig = px.area(global_daily, x='date', y='new_cases', 
                 labels={'new_cases': 'New Cases', 'date': 'Date'},
                 title="Daily New Cases Worldwide")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Country-specific Analysis")
    
    # Country trends
    st.subheader("Cases Development in Selected Countries")
    fig = px.line(df_filtered, x='date', y='total_cases', color='location',
                 labels={'total_cases': 'Total Cases', 'date': 'Date'},
                 title="Total Cases Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Mortality analysis
    st.subheader("Fatality Rate Analysis")
    df_filtered['fatality_rate'] = (df_filtered['total_deaths'] / df_filtered['total_cases']) * 100
    fig = px.line(df_filtered, x='date', y='fatality_rate', color='location',
                 labels={'fatality_rate': 'Fatality Rate (%)', 'date': 'Date'},
                 title="Case Fatality Rate Over Time")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Country Comparisons")
    
    # Top 20 countries
    st.subheader("Top 20 Countries by Total Cases")
    latest = df[df['date'] == df['date'].max()]
    top_countries = latest.nlargest(20, 'total_cases')[['location', 'total_cases', 'total_deaths']]
    
    fig = px.bar(top_countries, x='location', y='total_cases',
                labels={'total_cases': 'Total Cases', 'location': 'Country'},
                title="Total Cases by Country")
    st.plotly_chart(fig, use_container_width=True)
    
    # Map visualization
    st.subheader("Global Cases Distribution")
    fig = px.choropleth(latest, locations="iso_code",
                       color="total_cases",
                       hover_name="location",
                       color_continuous_scale=px.colors.sequential.Plasma,
                       title="Total COVID-19 Cases by Country")
    st.plotly_chart(fig, use_container_width=True)

# Raw data section
st.sidebar.header("About")
st.sidebar.info("Data source: Our World in Data COVID-19 Dataset")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw COVID-19 Data")
    st.write(df_filtered)