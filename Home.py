import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Nooriya's 🚀 Portfolio",
    page_icon="🎯",
    layout="centered"
)


# Main content with emojis
st.title("Nooriya's Portfolio")
st.subheader("🎓 IIT Madras | 💻 Data Science")

col1, col2 = st.columns([3, 2])
with col1:
    st.header("👋 About Me")
    st.write("""
    **8.25 CGPA Scholar** at IIT Madras  
    Passionate about **Data Science** & **Machine Learning** 
    Building intelligent systems that solve real-world problems  
    Constantly learning about AI & ML  
    """)
    with open("./resume.pdf", "rb") as file:  
        btn = st.download_button(
        label="📥 Download Resume",
        data=file,
        file_name="Nooriya_Resume.pdf",
        mime="application/pdf"
    )

    
with col2:
    # Add your image path here
    image = Image.open("profile.jpeg")  # Replace with your image
    st.image(image,) # caption="📸 Vansh at IIT Madras"

st.markdown("---")

# Projects
st.header("📂 Featured Projects")

col3, col4 = st.columns([2,2])
with col3:
    with st.expander("🏠 California House Price"):
        st.write("""
        **Tech Stack**: Python, Seaborn, Matplotlib, Scikit Learn  
        - Predicting house price based on its features    
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/California_House_Price) 🔗")

    with st.expander("📖 Book Recommendation"):
        st.write("""
        **Tech Stack**: Scikit Learn, Pickel, Pandas  
        - Recommending books based on selected fav. books  
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/Book_Recommendation) 🌐")

    with st.expander("📊 Linear Regression"):
        st.write("""
        **Tech Stack**: Numpy, Plotly, Matplotlib, Pandas  
        - Interactive Linear Regression with Gradient Descentt    
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/Linear_Regression) 🔗")

with col4:
    with st.expander("🧮 Monte Carlo π Estimation"):
        st.write("""
        **Tech Stack**: Numpy, Matplotlib  
        - Estimating π using Monte Carlo Simulation    
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/Monte_Carlo_%CF%80_Estimation) 🔗")

    with st.expander("🦠 Covid Visualization"):
        st.write("""
        **Tech Stack**: Streamlit, Numpy, Pandas, Plotly  
        - Visualizing the spread of covid 19 virus    
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/Covid) 🌐")

    with st.expander("🐧Penguine Classification"):
        st.write("""
        **Tech Stack**: Python, Scikit Learn, Numpy, Pandas  
        -  Classifying bread of penguine based on several parameters 
        """)
        st.markdown("[Live Demo](https://nooriya.streamlit.app/Penguine_Classification) 🔗")

st.markdown("---")


# Skills
st.header("🛠️ Technical Skills")
col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("💻 Languages")
    st.write("- Python")
    st.write("- SQL")

with col4:
    st.subheader("📚 Frameworks")
    st.write("- TensorFlow")
    st.write("- Scikit-Learn")
    st.write("- Numpy")
    st.write("- Pandas")
    st.write("- Seaborn")

with col5:
    st.subheader("🔧 Tools")
    st.write("- Google Sheets")
    st.write("- Power BI")
    st.write("- Excel")
    st.write("- Jupyter notebook")

st.markdown("---")


# Footer

st.markdown("### ❄️ Crafted by Nooriya")
st.markdown("###### Learning never stops")

