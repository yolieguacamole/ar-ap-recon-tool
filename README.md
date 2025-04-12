# 🌵 Reconciliation Dashboard by Mojave Technologies

A beautifully minimalist reconciliation tool built with Python and Streamlit. Upload invoice and payment data, visualize matches, and track discrepancies — all with a clean Mojave-branded interface.

<img src="data/logo.png" alt="Mojave Logo" width="200"/>

---

## 📊 Features

- Upload invoices & payments via CSV
- Fuzzy-matching using names + amounts (RapidFuzz)
- Summary metrics: matched, unmatched, unpaid
- Wes Anderson–inspired UI with custom branding
- Download final reconciliation results as CSV
- Placeholder dropdown for future financial system integrations

---

## 📂 Folder Structure

```
ar_ap_recon_tool/
├── app.py
├── reconciler.py
├── requirements.txt
├── README.md
├── data/
│   ├── logo.png
│   ├── sample_invoices.csv
│   └── sample_payments.csv
└── .streamlit/
    └── config.toml
```

---

## 🚀 How to Run Locally

1. Clone the repo:

```bash
git clone https://github.com/yolieguacamole/ar-ap-recon-tool.git
cd ar-ap-recon-tool
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

---

## 🌐 How to Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub and select this repo
4. Set `app.py` as the entry point and deploy!

---

### 💾 Sample Files
You can test it using the included `data/sample_invoices.csv` and `data/sample_payments.csv`.
