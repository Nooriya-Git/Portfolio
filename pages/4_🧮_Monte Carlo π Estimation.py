import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="π Monte Carlo Simulation", layout="centered")

# Initialize session state for storing points
if 'points' not in st.session_state:
    st.session_state.points = {'x': [], 'y': [], 'inside': []}

# App title and description
st.title("🧮 Estimating π using Monte Carlo Simulation")
st.link_button(label= "👨‍💻 Github Repo" , url="https://github.com")
st.markdown("""
This app estimates the value of π using the Monte Carlo method with dart throws:
1. Darts are randomly thrown at a square board (length = 2)
2. We check if they land inside the inscribed circle (radius = 1)
3. π is estimated using the ratio: (Points inside circle / Total points) × 4
""")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    n = st.slider("Number of dart throws", 
                 min_value=0, 
                 max_value=1000000, 
                 value=1000, 
                 step=100,
                 help="Adjust the number of darts to throw")
    
    if st.button("Reset Simulation"):
        st.session_state.points = {'x': [], 'y': [], 'inside': []}

# Main content
col1, col2 = st.columns(2)

with col1:
    st.header("Simulation Results")
    
    # Generate new points when needed
    current_points = len(st.session_state.points['x'])
    if n > current_points:
        new_points = n - current_points
        new_x = np.random.uniform(-1, 1, new_points)
        new_y = np.random.uniform(-1, 1, new_points)
        new_inside = (new_x**2 + new_y**2) <= 1
        
        st.session_state.points['x'].extend(new_x)
        st.session_state.points['y'].extend(new_y)
        st.session_state.points['inside'].extend(new_inside.tolist())
    elif n < current_points:
        st.session_state.points['x'] = st.session_state.points['x'][:n]
        st.session_state.points['y'] = st.session_state.points['y'][:n]
        st.session_state.points['inside'] = st.session_state.points['inside'][:n]

    # Convert to numpy arrays for easier handling
    x = np.array(st.session_state.points['x'])
    y = np.array(st.session_state.points['y'])
    inside = np.array(st.session_state.points['inside'])
    
    # Calculate π estimate
    if n > 0:
        pi_estimate = 4 * np.sum(inside) / n
    else:
        pi_estimate = 0
        
    # Display metrics
    st.metric("Estimated π", f"{pi_estimate:.5f}")
    st.metric("Actual π", f"{np.pi:.5f}")
    st.metric("Difference", f"{abs(np.pi - pi_estimate):.5f}")

with col2:
    st.header("Visualization")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f0f0')
    
    # Draw circle
    circle = plt.Circle((0, 0), 1, color='green', fill=False, linewidth=2)
    ax.add_patch(circle)
    
    # Plot points if we have any
    if n > 0:
        ax.scatter(x[inside], y[inside], color='blue', s=5, alpha=0.5, label='Inside Circle')
        ax.scatter(x[~inside], y[~inside], color='red', s=5, alpha=0.5, label='Outside Circle')
        ax.legend(loc='upper right')
    
    # Add grid and labels
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title("Dart Throws Visualization")
    
    st.pyplot(fig)

# Explanation
st.markdown("""
### How It Works
- **Monte Carlo Simulation**: This method uses random sampling to estimate mathematical constants
- **Dart Throws**: Random points are generated within a square (-1 ≤ x ≤ 1, -1 ≤ y ≤ 1)
- **Circle Equation**: Points inside the circle satisfy x² + y² ≤ 1
- **π Estimation**: The ratio of inside/total points approaches π/4 as more darts are thrown
""")