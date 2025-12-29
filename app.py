
import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Customer Satisfaction Predictor",
    page_icon="😊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        font-size: 16px;
        border-radius: 5px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🎯 Customer Satisfaction Prediction System")
st.markdown("---")
st.markdown("""
This application predicts customer satisfaction ratings (1-5) based on support ticket information.
Enter the ticket details below to get a prediction.
""")

# Load the models and preprocessing objects
@st.cache_resource
def load_models():
    try:
        with open('random_forest_model.pkl', 'rb') as f:
            rf_model = pickle.load(f)
        with open('logistic_regression_model.pkl', 'rb') as f:
            lr_model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('label_encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        return rf_model, lr_model, scaler, encoders
    except FileNotFoundError:
        st.error("Model files not found! Please ensure all .pkl files are in the same directory.")
        return None, None, None, None

rf_model, lr_model, scaler, encoders = load_models()

if rf_model and lr_model and scaler and encoders:
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Customer Information")
        customer_age = st.slider("Customer Age", min_value=18, max_value=70, value=35, step=1)
        customer_gender = st.selectbox("Customer Gender", options=['Male', 'Female', 'Other'])
        
        st.subheader("🎫 Ticket Details")
        ticket_type = st.selectbox("Ticket Type", options=[
            'Technical issue', 
            'Billing inquiry', 
            'Product inquiry', 
            'Refund request', 
            'Cancellation request'
        ])
        
        ticket_subject = st.selectbox("Ticket Subject", options=[
            'Software bug', 'Hardware issue', 'Network problem',
            'Product setup', 'Installation support', 'Battery life',
            'Product compatibility', 'Peripheral compatibility',
            'Data loss', 'Account access', 'Payment issue',
            'Refund request', 'Cancellation request', 'Delivery problem',
            'Product recommendation', 'Display issue'
        ])
    
    with col2:
        st.subheader("🛍️ Product Information")
        product_purchased = st.selectbox("Product Purchased", options=[
            'iPhone', 'Samsung Galaxy', 'Dell XPS', 'MacBook Pro', 'Lenovo ThinkPad',
            'HP Pavilion', 'Microsoft Surface', 'Asus ROG', 'Sony PlayStation',
            'Xbox', 'Nintendo Switch', 'LG Smart TV', 'Sony 4K HDR TV',
            'Canon EOS', 'Nikon D', 'GoPro Hero', 'Amazon Echo', 'Google Nest',
            'Apple AirPods', 'Bose QuietComfort', 'Fitbit Charge', 'Microsoft Office',
            'Adobe Photoshop', 'Autodesk AutoCAD'
        ])
        
        st.subheader("⚙️ Ticket Settings")
        ticket_priority = st.selectbox("Ticket Priority", options=['Low', 'Medium', 'High', 'Critical'])
        ticket_channel = st.selectbox("Ticket Channel", options=['Email', 'Phone', 'Chat', 'Social media'])
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Predict Customer Satisfaction"):
        # Create input dataframe
        input_data = pd.DataFrame({
            'Customer Age': [customer_age],
            'Customer Gender': [customer_gender],
            'Product Purchased': [product_purchased],
            'Ticket Type': [ticket_type],
            'Ticket Subject': [ticket_subject],
            'Ticket Priority': [ticket_priority],
            'Ticket Channel': [ticket_channel]
        })
        
        # Encode categorical variables
        input_encoded = input_data.copy()
        for column in encoders.keys():
            try:
                input_encoded[column] = encoders[column].transform(input_encoded[column])
            except ValueError:
                st.error(f"Unknown value for {column}. Please select from available options.")
                st.stop()
        
        # Scale features
        input_scaled = scaler.transform(input_encoded)
        
        # Make predictions
        rf_prediction = rf_model.predict(input_scaled)[0]
        lr_prediction = lr_model.predict(input_scaled)[0]
        
        # Display predictions
        st.markdown("---")
        st.subheader("📊 Prediction Results")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.markdown("""
                <div class="prediction-box">
                    <h3 style="text-align: center;">Random Forest</h3>
                    <h1 style="text-align: center; color: #4CAF50;">⭐ {:.0f}</h1>
                    <p style="text-align: center;">Predicted Rating</p>
                </div>
            """.format(rf_prediction), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="prediction-box">
                    <h3 style="text-align: center;">Logistic Regression</h3>
                    <h1 style="text-align: center; color: #2196F3;">⭐ {:.0f}</h1>
                    <p style="text-align: center;">Predicted Rating</p>
                </div>
            """.format(lr_prediction), unsafe_allow_html=True)
        
        with col5:
            avg_prediction = (rf_prediction + lr_prediction) / 2
            st.markdown("""
                <div class="prediction-box">
                    <h3 style="text-align: center;">Average</h3>
                    <h1 style="text-align: center; color: #FF9800;">⭐ {:.1f}</h1>
                    <p style="text-align: center;">Ensemble Prediction</p>
                </div>
            """.format(avg_prediction), unsafe_allow_html=True)
        
        # Interpretation
        st.markdown("---")
        st.subheader("📝 Interpretation")
        
        satisfaction_level = ""
        if avg_prediction <= 2:
            satisfaction_level = "😟 **Low Satisfaction** - Immediate attention required!"
            color = "#f44336"
        elif avg_prediction <= 3:
            satisfaction_level = "😐 **Moderate Satisfaction** - Room for improvement"
            color = "#ff9800"
        else:
            satisfaction_level = "😊 **High Satisfaction** - Customer likely to be happy"
            color = "#4caf50"
        
        st.markdown(f'<p style="font-size: 20px; color: {color};">{satisfaction_level}</p>', 
                   unsafe_allow_html=True)
        
        # Show input summary
        with st.expander("📋 View Input Summary"):
            st.write(input_data)

# Sidebar with information
st.sidebar.title("ℹ️ About")
st.sidebar.info("""
**Customer Satisfaction Predictor**

This application uses machine learning to predict customer satisfaction ratings based on support ticket information.

**Models Used:**
- Random Forest Classifier
- Logistic Regression

**Features Considered:**
- Customer Age
- Customer Gender
- Product Purchased
- Ticket Type
- Ticket Subject
- Ticket Priority
- Ticket Channel

**Rating Scale:**
- 1: Very Dissatisfied
- 2: Dissatisfied
- 3: Neutral
- 4: Satisfied
- 5: Very Satisfied
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Model Accuracy:** ~20%")
st.sidebar.warning("⚠️ Predictions are estimates and should be used as guidance only.")
