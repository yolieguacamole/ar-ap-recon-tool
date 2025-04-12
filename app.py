import streamlit as st
import pandas as pd
from reconciler import load_data, reconcile, get_summary_stats
import time

st.set_page_config(page_title="AR/AP Reconciliation Tool", layout="wide")

# 🌟 Styled Header
st.markdown("""
    <style>
    .big-font {
        font-size:32px !important;
        font-weight:600;
    }
    .subtext {
        font-size:16px;
        color: gray;
    }
    .stMetric { font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🔍 AR/AP Reconciliation Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Track and analyze your financial reconciliation results across invoices and payments.</p>', unsafe_allow_html=True)

# Upload section
col1, col2 = st.columns(2)

with col1:
    invoice_file = st.file_uploader("📄 Upload Invoice CSV", type="csv")

with col2:
    payment_file = st.file_uploader("💳 Upload Payment CSV", type="csv")

# Load uploaded or default data
if invoice_file and payment_file:
    invoices, payments = load_data(invoice_file, payment_file)
else:
    st.warning("📁 No files uploaded — loading test data from `data/` folder for development.")
    invoices, payments = load_data("data/sample_invoices.csv", "data/sample_payments.csv")

# Reconcile and summarize
results = reconcile(invoices, payments)
summary = get_summary_stats(results)

# Metrics
st.subheader("📊 Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Invoices", summary['Total Invoices'])
col2.metric("Matched", summary['Matched'])
col3.metric("Unmatched Payments", summary['Unmatched Payments'])
col4.metric("Unpaid Invoices", summary['Unpaid Invoices'])

# Dataframe
st.subheader("🧾 Detailed Reconciliation Results")
st.dataframe(results, use_container_width=True)

# Download
csv = results.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Results as CSV", csv, "reconciliation_results.csv", "text/csv")

# 🔗 API Integration Section
st.subheader("🔌 Financial System Integration (Coming Soon)")
st.markdown("You'll soon be able to connect this dashboard to financial systems like QuickBooks, NetSuite, and Oracle Fusion.")

# System selector
with st.container():
    st.markdown("**Connect System:**")
    system = st.selectbox(
        "",
        ["QuickBooks Online", "NetSuite", "Oracle Fusion", "Salesforce"],
        label_visibility="collapsed"  # Hides extra label spacing
    )

# Simulated connect button
if st.button("🔄 Connect to API"):
    with st.spinner(f"Connecting to {system}..."):
        time.sleep(2)
    st.success(f"✅ Connected to {system} (simulated)")