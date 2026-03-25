# 🛍️ E-commerce Purchase Propensity Engine

An end-to-end Machine Learning pipeline built on **Google Cloud Platform (GCP)** to predict customer conversion behavior with high precision.

---

## 📊 Project Performance
- **Accuracy:** 93.7%
- **ROC-AUC:** 0.9785
- **Dataset:** 0.9 Million+ Web Sessions (Google Analytics Sample)

---

## 🛠️ Tech Stack & Tools
- **Cloud Warehouse:** Google BigQuery
- **Machine Learning:** BigQuery ML (Logistic Regression)
- **MLOps:** MLflow (Experiment Tracking & Versioning)
- **Interface:** Streamlit (Real-time Inference Dashboard)
- **Languages:** SQL, Python

---

##  The Data Science Challenge: Target Leakage
The biggest hurdle in this project was **Target Leakage**. Initially, the model achieved 100% accuracy because it was training on features that occur *after* a purchase (e.g., checkout page hits). 
**Solution:** - Filtered behavioral data to only include pre-transactional events.
- Engineered session-level features: `pageviews`, `time_on_site`, and `operating_system`.
- Balanced the dataset using `AUTO_CLASS_WEIGHTS`.

---

##  Key Features of the Dashboard
- **Real-time Inference:** Connects directly to BigQuery via Python API.
- **Dynamic Thresholding:** Allows business users to adjust classification boundaries (Precision-Recall trade-off).
- **Feature Influence:** Visualizes how different user behaviors impact the final probability.
- **Dashboard Link:** https://ecommerce-conversion-predictor-mlops-5gyscnkrhnpqdgjfawsvw6.streamlit.app/

---

## 📂 Project Structure
```text
├── app.py                # Streamlit Application Code
├── sql_queries/          # BigQuery ML Training & Preprocessing scripts
├── requirements.txt      # Project Dependencies
├── .gitignore            # Security: Hiding GCP Credentials (key.json)
└── README.md             # Project Documentation
