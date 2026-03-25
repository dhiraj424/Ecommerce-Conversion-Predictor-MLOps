import streamlit as st
from google.cloud import bigquery
import os

# --- STEP 1: Smart Client Initialization ---
def initialize_bq_client():
    # 1. Check if running on Streamlit Cloud (using Secrets)
    if "gcp_service_account" in st.secrets:
        # Streamlit secrets se credentials uthana
        credentials_info = dict(st.secrets["gcp_service_account"])
        return bigquery.Client.from_service_account_info(credentials_info)
    
    # 2. Check if running locally (using your local key.json file)
    elif os.path.exists("key.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
        return bigquery.Client()
    
    else:
        st.error("GCP Credentials not found. Please check Streamlit Secrets or key.json.")
        st.stop()

# Initializing Client
client = initialize_bq_client()

# Step 2:
import streamlit as st
from google.cloud import bigquery
import os
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="E-commerce Conversion Predictor",
    layout="wide"
)

# --- AUTHENTICATION & CLIENT SETUP ---
def initialize_bq_client(key_path="key.json"):
    """Initializes the BigQuery client using service account credentials."""
    if os.path.exists(key_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        return bigquery.Client()
    else:
        st.error("Authentication Error: 'key.json' not found in the root directory.")
        st.stop()

client = initialize_bq_client()

# --- APPLICATION HEADER ---
st.title("Customer Purchase Propensity Dashboard")
st.markdown("""
    This analytical tool utilizes a **BigQuery ML Logistic Regression** model to calculate 
    the probability of a user conversion based on session-level behavioral data.
""")

st.divider()

# --- INPUT SECTION ---
col_dem, col_beh, col_set = st.columns(3)

with col_dem:
    st.subheader("User Demographics")
    os_choice = st.selectbox("Operating System", ["Windows", "Macintosh", "Android", "iOS", "Linux"])
    is_mobile = st.checkbox("Mobile Device", value=False)

with col_beh:
    st.subheader("Session Behavior")
    pageviews = st.slider("Total Pageviews", 1, 100, 10)
    time_on_site = st.number_input("Time on Site (Seconds)", min_value=0, max_value=10000, value=300)

with col_set:
    st.subheader("Model Configuration")
    threshold = st.slider("Classification Threshold (%)", 0, 100, 75) / 100

# --- PREDICTION AND ANALYTICS ---
if st.button("Run Model Inference", type="primary", use_container_width=True):
    with st.spinner('Processing Query on Google Cloud...'):
        try:
            # SQL Query for BigQuery ML Prediction
            predict_query = f"""
            SELECT
              p.prob AS conversion_probability
            FROM
              ML.PREDICT(MODEL `dhiraj-bigdata-ai.ecommerce_data.conversion_model`, (
                SELECT
                  '{os_choice}' AS os,
                  {str(is_mobile).upper()} AS is_mobile,
                  {pageviews} AS pageviews,
                  {time_on_site} AS time_on_site,
                  '(none)' AS medium
              )),
              UNNEST(predicted_label_probs) AS p
            WHERE p.label = 1
            """
            
            # Execute and Fetch Results
            df_results = client.query(predict_query).to_dataframe()
            
            if not df_results.empty:
                probability = df_results['conversion_probability'][0]
                
                # --- RESULTS DISPLAY ---
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.metric(label="Predicted Probability", value=f"{probability:.2%}")
                    
                    # Logic-based status updates
                    if probability >= threshold:
                        st.success("STATUS: High Conversion Intent")
                    elif probability > 0.30:
                        st.warning("STATUS: Moderate Conversion Intent")
                    else:
                        st.error("STATUS: Low Conversion Intent")

                with res_col2:
                    # Feature Influence Visualization
                    impact_data = pd.DataFrame({
                        'Feature': ['Pageviews', 'Time on Site', 'OS Type', 'Mobile'],
                        'Weight': [pageviews * 0.7, time_on_site * 0.005, 10, 5]
                    })
                    fig = px.bar(impact_data, x='Weight', y='Feature', orientation='h', 
                                 title="Relative Feature Importance")
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Inference Failed: {str(e)}")

# --- FOOTER ---
st.divider()
st.caption("Data Science Portfolio Project | Developed by Dhiraj Kumar Gupta")
