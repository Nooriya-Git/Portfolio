# house_price_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
california = fetch_california_housing()
df = pd.DataFrame(california.data, columns=california.feature_names)
df['Price'] = california.target

# Streamlit app
st.title('🏠 California House Price Prediction')
st.write('Predicting house prices using machine learning')
st.header('House Features')
# Main layout columns
col1, col2 = st.columns([1, 1])

# ===== LEFT COLUMN (Inputs) =====

with col1:    
    med_inc = st.slider('Median Income', float(df['MedInc'].min()), float(df['MedInc'].max()), float(df['MedInc'].median()))
    house_age = st.slider('House Age', float(df['HouseAge'].min()), float(df['HouseAge'].max()), float(df['HouseAge'].median()))
    rooms = st.slider('Avg Rooms', float(df['AveRooms'].min()), float(df['AveRooms'].max()), float(df['AveRooms'].median()))
    bedrooms = st.slider('Avg Bedrooms', float(df['AveBedrms'].min()), float(df['AveBedrms'].max()), float(df['AveBedrms'].median()))

with col2:
    population = st.slider('Population', float(df['Population'].min()), float(df['Population'].max()), float(df['Population'].median()))
    occupancy = st.slider('Occupancy', float(df['AveOccup'].min()), float(df['AveOccup'].max()), float(df['AveOccup'].median()))
    latitude = st.slider('Latitude', float(df['Latitude'].min()), float(df['Latitude'].max()), float(df['Latitude'].median()))
    longitude = st.slider('Longitude', float(df['Longitude'].min()), float(df['Longitude'].max()), float(df['Longitude'].median())) 

# ===== MODEL TRAINING =====
X = df.drop('Price', axis=1)
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_type = st.sidebar.selectbox('Select Model', ['Linear Regression', 'Random Forest'])
model = LinearRegression() if model_type == 'Linear Regression' else RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Create input array
input_data = np.array([[med_inc, house_age, rooms, bedrooms, population, occupancy, latitude, longitude]])
prediction = model.predict(input_data)[0]



st.header('Prediction Results')

# Big bold price display
if prediction<0:
    st.markdown(f"<h2>$0</h2>", 
            unsafe_allow_html=True)
else:
    st.markdown(f"<h2>${prediction*100000:,.2f}</h2>", 
                unsafe_allow_html=True)

# Feature importance
if model_type == 'Random Forest':
    st.subheader('Feature Importance')
    importance = pd.Series(model.feature_importances_, index=X.columns)
    fig_imp, ax_imp = plt.subplots()
    importance.sort_values().plot.barh(ax=ax_imp)
    st.pyplot(fig_imp)
else:
    st.write("Feature importance not available for Linear Regression")

# ===== VISUALIZATION GRID =====
st.header("Data Visualizations")

# Create plots
fig1, ax1 = plt.subplots()
sns.histplot(df['Price'], kde=True, ax=ax1)
ax1.set_title('Price Distribution')


fig3, ax3 = plt.subplots(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax3)
ax3.set_title('Feature Correlation')

# Create grid
col3, col4 = st.columns(2)
with col3:
    st.pyplot(fig1)
    
with col4:
    st.pyplot(fig3)
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df.head())

# Model metrics in sidebar
st.sidebar.header('Model Performance')
st.sidebar.write(f'**{model_type} Results**')
st.sidebar.write(f'R² Score: {r2_score(y_test, y_pred):.2f}')
st.sidebar.write(f'MSE: {mean_squared_error(y_test, y_pred):.2f}')
