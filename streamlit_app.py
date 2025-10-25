import streamlit as st
import requests
import json

# Configure the page
st.set_page_config(
    page_title="Gemstone Price Predictor",
    page_icon="💎",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        margin-top: 0.5rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .price-result {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff4b4b;
        text-align: center;
    }
    .info-section {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# API configuration
API_URL = "http://localhost:8000"  # Change if deployed

def predict_price(data):
    """Send prediction request to FastAPI backend"""
    try:
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"API Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Connection error: {str(e)}"}

def main():
    # Header
    st.markdown('<h1 class="main-header">💎 Gemstone Price Predictor</h1>', unsafe_allow_html=True)
    
    # Create three columns for input fields
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📏 Physical Characteristics")
        carat = st.slider("Carat Weight", min_value=0.2, max_value=5.0, value=1.0, step=0.1)
        depth = st.slider("Depth (%)", min_value=40.0, max_value=80.0, value=62.5, step=0.1)
        table = st.slider("Table (%)", min_value=40.0, max_value=80.0, value=58.0, step=0.1)
    
    with col2:
        st.subheader("📐 Dimensions (mm)")
        x = st.slider("Length (x)", min_value=3.0, max_value=10.0, value=5.7, step=0.1)
        y = st.slider("Width (y)", min_value=3.0, max_value=10.0, value=5.7, step=0.1)
        z = st.slider("Height (z)", min_value=2.0, max_value=8.0, value=3.5, step=0.1)
    
    with col3:
        st.subheader("💎 Quality Grades")
        cut = st.selectbox("Cut Quality", ["Ideal", "Premium", "Very Good", "Good", "Fair"])
        color = st.selectbox("Color Grade", ["D", "E", "F", "G", "H", "I", "J"])
        clarity = st.selectbox("Clarity", ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"])
    
    # API status check (moved from sidebar)
    st.markdown("---")
    col_status1, col_status2 = st.columns([3, 1])
    
    with col_status2:
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Failed")
        except:
            st.error("❌ No Connection")
    
    # Predict button
    if st.button("🚀 Predict Price", use_container_width=True, type="primary"):
        # Prepare data for API
        input_data = {
            "carat": carat,
            "depth": depth,
            "table": table,
            "x": x,
            "y": y,
            "z": z,
            "cut": cut,
            "color": color,
            "clarity": clarity
        }
        
        # Show loading spinner
        with st.spinner("Calculating price..."):
            result = predict_price(input_data)
        
        # Display results
        if result["status"] == "success":
            st.markdown("---")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 Input Summary")
                st.json(input_data)
            
            with col2:
                st.subheader("💰 Prediction Result")
                st.markdown(f'<div class="price-result">${result["predicted_price"]:,.2f}</div>', unsafe_allow_html=True)
                st.success("Price prediction completed successfully!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show raw API response in expander
            with st.expander("📋 View Raw API Response"):
                st.json(result)
                
        else:
            st.error(f"❌ {result['message']}")

if __name__ == "__main__":
    main()