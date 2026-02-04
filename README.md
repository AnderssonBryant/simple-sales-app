# ☕ Coffee Shop Sales Management App (Streamlit)

A local-first coffee shop sales logging and reporting system built with **Python and Streamlit**.  
This project is designed as a **portfolio demo application** that simulates real-world sales workflows, reporting pipelines, and financial summaries.

The system focuses on simplicity, reproducibility, and analytics-oriented design.

---

## 🚀 Features

### Sales Management
- Bulk daily sales input per product
- Automatic revenue calculation
- Sales history table (latest-first ordering)
- Zero-quantity products automatically excluded

### Reporting
- Custom date range sales summary
- Sales report PDF export with automatic download
- Cashflow summary (inflow vs outflow)
- Expense report table

### Analytics
- Sales trend line chart (date-indexed)
- Product sales distribution bar chart

### Data System
- CSV-based local storage (offline-first)
- Standalone data seeding pipeline
- Reproducible demo dataset generation

---

## 🧱 Project Structure

DailySalesLogger/
│
├── app.py # Streamlit application
├── requirements.txt
├── README.md
│
└── data/
├── menu.csv
├── daily_sales.csv
├── expenses.csv
└── cashflow.csv

---

## 📄 PDF Export Capability

The application supports:

- Sales summary export to PDF
- Automatic browser download
- Clean table layout
- Product name mapping from menu reference

This simulates real operational reporting workflows.

---

## 🎯 Project Objective

This project was built to demonstrate:

- Python data processing skills
- Streamlit dashboard development
- Reporting automation
- Data pipeline thinking
- Local-first application design

It is intended for **portfolio demonstration and educational use**, not production POS deployment.

---

## 🔧 Planned Improvements

Potential future enhancements:

- SQLite database backend
- Authentication system
- Inventory stock management
- Multi-user access roles
- Cloud deployment option
- API-based data ingestion

---

## 📜 License

Open-source project for learning and portfolio demonstration purposes.
