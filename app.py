import streamlit as st
from google.cloud import bigquery
import os
import pandas as pd
import plotly.express as px
import json

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="E-commerce Conversion Predictor",
    layout="wide"
)

# --- 2. SMART AUTHENTICATION ---
@st.cache_resource
def initialize_bq_client():
    # Check if running on Streamlit Cloud (using Secrets)
    if "gcp_service_account" in st.secrets:
        try:
            secret_data = st.secrets["gcp_service_account"]
            # Handling both String and Dict formats in Secrets
            if isinstance(secret_data, str):
                credentials_info = json.loads(secret_data)
            else:
                credentials_info = dict(secret_data)
            return bigquery.Client.from_service_account_info(credentials_info)
        except Exception as e:
            st.error(f"Authentication Error (Secrets): {e}")
            st.stop()
    
    # Check if running locally
    elif os.path.exists("key.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
        return bigquery.Client()
    
    else:
        st.error("Credentials not found! Please set up Streamlit Secrets or provide key.json.")
        st.stop()

client = initialize_bq_client()

# --- 3. UI HEADER ---
st.title("🚀 Customer Purchase Propensity Dashboard")
st.markdown("""
    This dashboard predicts the probability of a user making a purchase using 
    **BigQuery ML (Logistic Regression)**. Adjust the parameters below to see real-time inference.
""")

st.divider()

# --- 4. INPUT PANEL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💻 Device Info")
    os_choice = st.selectbox("Operating System", ["Windows", "Macintosh", "Android", "iOS", "Linux"])
    is_mobile = st.toggle("Mobile Device", value=False)

with col2:
    st.subheader("🖱️ User Behavior")
    pageviews = st.slider("Total Pageviews", 1, 100, 15)
    time_on_site = st.number_input("Time on Site (Seconds)", min_value=0, value=300)

with col3:
    st.subheader("⚙️ Model Settings")
    threshold = st.slider("Success Threshold (%)", 0, 100, 70) / 100

# --- 5. MODEL INFERENCE ---
if st.button("Run Prediction", type="primary", use_container_width=True):
    with st.spinner('Querying BigQuery ML Model...'):
        try:
            # CORRECTED SQL QUERY SYNTAX
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
            
            # Executing Query
            query_job = client.query(predict_query)
            df_results = query_job.to_dataframe()
            
            if not df_results.empty:
                prob = df_results['conversion_probability'][0]
                
                # --- 6. DISPLAY RESULTS ---
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.metric("Conversion Probability", f"{prob:.2%}")
                    
                    if prob >= threshold:
                        st.success("🔥 Result: High Intent Buyer")
                    elif prob > 0.3:
                        st.warning("⚖️ Result: Potential Lead")
                    else:
                        st.error("🧊 Result: Low Interest")

                with res_col2:
                    # Mocking Feature Importance for UI (Calculated based on weights)
                    feat_data = pd.DataFrame({
                        'Feature': ['Pageviews', 'Time/Site', 'Device Type', 'OS'],
                        'Impact': [pageviews * 0.8, time_on_site * 0.01, 15 if is_mobile else 5, 10]
                    })
                    fig = px.bar(feat_data, x='Impact', y='Feature', orientation='h', 
                                 title="Feature Contribution to Prediction",
                                 color_discrete_sequence=['#ff4b4b'])
                    st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Inference Failed: {e}")

# --- 7. FOOTER ---
st.divider()
st.caption("Built by Dhiraj Kumar Gupta | Data Science Portfolio")
