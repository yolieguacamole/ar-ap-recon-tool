import streamlit as st
import pandas as pd
from reconciler import load_data, reconcile, get_summary_stats
import time

st.set_page_config(page_title="Reconciliation Dashboard", layout="wide")

# Logo and header section
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("data/logo.png", width=180)
with col_title:
    st.markdown("<h2 style='margin-bottom:0;'>Reconciliation Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#666;'>A pastel-flavored tool for matching invoices and payments.</p>", unsafe_allow_html=True)

st.markdown("---")

# Upload section
col1, col2 = st.columns(2)
with col1:
    invoice_file = st.file_uploader("📄 Upload Invoice CSV", type="csv")
with col2:
    payment_file = st.file_uploader("💳 Upload Payment CSV", type="csv")

# Load data
if invoice_file and payment_file:
    invoices, payments = load_data(invoice_file, payment_file)
else:
    st.warning("📁 No files uploaded — loading sample data.")
    invoices, payments = load_data("data/sample_invoices.csv", "data/sample_payments.csv")

results = reconcile(invoices, payments)
summary = get_summary_stats(results)

# Summary Metrics
st.subheader("📊 Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Invoices", summary['Total Invoices'])
col2.metric("Matched", summary['Matched'])
col3.metric("Unmatched Payments", summary['Unmatched Payments'])
col4.metric("Unpaid Invoices", summary['Unpaid Invoices'])

# Table View
st.subheader("🧾 Detailed Results")
st.dataframe(results, use_container_width=True)

# Download Button
csv = results.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download CSV", csv, "reconciliation_results.csv", "text/csv")

# Integration Preview
st.subheader("🔌 Financial System Integration (Coming Soon)")
system = st.selectbox("Choose system", ["QuickBooks", "NetSuite", "Oracle", "Salesforce"])
if st.button("🔄 Connect (simulated)"):
    with st.spinner("Connecting..."):
        time.sleep(1.5)
    st.success(f"Connected to {system} (placeholder)")