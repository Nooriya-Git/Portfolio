import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Load data
def load_data():
    data = pd.read_csv('income_data.csv')
    return data[['Age', 'Income']]

data = load_data()

# Streamlit app
st.set_page_config(page_title="Linear Regression", layout="wide")
st.title('📈 Interactive Linear Regression with Gradient Descentt')
st.markdown("""
Explore how gradient descent optimizes linear regression parameters!
""")

# Sidebar controls
st.sidebar.header('Controls')
m_init = st.sidebar.slider('Initial slope (m)', -5.0, 5.0, 0.0)
b_init = st.sidebar.slider('Initial intercept (b)', -20000, 20000, 0)
learning_rate = st.sidebar.slider('Learning rate', 0.0001, 0.01, 0.001)
epochs = st.sidebar.slider('Epochs', 10, 5000, 50)

# Prepare data
X = data['Age'].values
y = data['Income'].values
n = len(X)

# Normalize data
X_mean, X_std = X.mean(), X.std()
y_mean, y_std = y.mean(), y.std()
X_normalized = (X - X_mean) / X_std
y_normalized = (y - y_mean) / y_std

# Gradient descent implementation
def gradient_descent(m, b, X, y, learning_rate, epochs):
    m_values = [m]
    b_values = [b]
    errors = []
    
    for _ in range(epochs):
        y_pred = m * X + b
        error = (1/n) * np.sum((y_pred - y) ** 2)
        errors.append(error)
        
        # Calculate gradients
        dm = (2/n) * np.sum(X * (y_pred - y))
        db = (2/n) * np.sum(y_pred - y)
        
        # Update parameters
        m -= learning_rate * dm
        b -= learning_rate * db
        
        m_values.append(m)
        b_values.append(b)
    
    return m_values, b_values, errors

# Run gradient descent when button clicked
if st.sidebar.button('Run Gradient Descent'):
    m_history, b_history, error_history = gradient_descent(
        m_init, b_init, X_normalized, y_normalized, learning_rate, epochs
    )
    
    # Create 3D surface plot
    st.subheader('3D Error Landscape with Gradient Descent Path')
    
    # Generate grid for error surface
    m_range = np.linspace(min(m_history)-0.5, max(m_history)+0.5, 50)
    b_range = np.linspace(min(b_history)-0.5, max(b_history)+0.5, 50)
    M, B = np.meshgrid(m_range, b_range)
    
    # Calculate MSE for grid points
    Z = np.zeros(M.shape)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            Z[i,j] = np.mean((M[i,j] * X_normalized + B[i,j] - y_normalized) ** 2)
    col1, col2 = st.columns(2)

    

    with col1:
        # Create 3 D plot
        fig = go.Figure(data=[
            go.Surface(z=Z, x=M, y=B, colorscale='Viridis', opacity=0.7),
            go.Scatter3d(x=m_history, y=b_history, z=error_history, 
                        mode='lines+markers', marker=dict(size=4), 
                        line=dict(color='red', width=2))
        ],)

        
        fig.update_layout(height=600, scene=dict(
            xaxis_title='Slope (m)',
            yaxis_title='Intercept (b)',
            zaxis_title='Error (MSE)',
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1))
        ))
        
        st.plotly_chart(fig, use_container_height =True)
    with col2:
        # Show final regression line
        st.subheader('Final Regression Line')
        
        # Proper denormalization
        final_m = m_history[-1] * y_std / X_std
        final_b = (b_history[-1] * y_std) + y_mean - (final_m * X_mean)
        
        # Calculate best fit line properties
        x_min, x_max = X.min(), X.max()
        y_pred_min = final_m * x_min + final_b
        y_pred_max = final_m * x_max + final_b
        
        fig2, ax = plt.subplots()
        ax.scatter(X, y, alpha=0.5, label='Actual Data')
        ax.plot([x_min, x_max], [y_pred_min, y_pred_max], 
            color='red', linewidth=2, label='Regression Line')
        ax.set_xlabel('Age')
        ax.set_ylabel('Income')
        ax.legend()
        st.pyplot(fig2)
    
    # Show equations and explanations
    st.subheader('Final Equation')
    st.markdown(f"""
    $$
    y = {final_m:.2f}x + {final_b:.2f}
    $$
    """)

else:
    st.info('👈 Adjust parameters and click "Run Gradient Descent" to start!')

# Show raw data
st.subheader('Raw Data')
st.dataframe(data, height=150)
