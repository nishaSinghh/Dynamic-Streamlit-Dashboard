# 📊 Dynamic Superstore Analytics Dashboard (v2.0)

A full-stack, multipage business intelligence application built with **Streamlit**, **Plotly**, and **SQLite**. This dashboard features a secure authentication system and provides real-time insights into retail sales, profit margins, and regional performance.

## 🚀 Live Demo
[https://nisha-dynamic-dashboard.streamlit.app/]

---

## ✨ Key Features

### 🛡️ Secure User Authentication
* **Custom Login/Signup System:** Powered by a local **SQLite** database for user credential management.
* **Session Persistence:** State-aware navigation that protects dashboard routes from unauthorized access.
* **Modern UI:** Responsive "Hero Section" login page with glassmorphism CSS effects.

### 📈 Advanced Data Visualization
* **Real-time KPI Tracking:** Instant calculation of Total Sales, Profit, and Order Counts.
* **Hierarchical Analysis:** Deep-dive into data using **Treemaps** (Region > Category > Sub-Category).
* **Time Series Forecasting:** Sales trend analysis over time with interactive line charts.
* **Relationship Mapping:** Sales vs. Profit correlation using dynamic Scatter Plots.

### 🛠️ Interactive Functionality
* **Dynamic Multi-Filters:** Sidebar filters for Region, State, and City that update content in real-time.
* **Custom File Support:** Upload your own `.csv`, `.xlsx`, or `.xls` files to analyze custom datasets on the fly.
* **Export Options:** Download filtered data as CSV files directly from the interface.

---

## 🛠️ Technology Stack
* **Frontend:** Streamlit (Python)
* **Visuals:** Plotly Express & Plotly Figure Factory
* **Database:** SQLite3 (Local storage for users)
* **Data Processing:** Pandas, NumPy
* **Styling:** Custom CSS & Matplotlib (for background gradients)

---

## 📁 Project Structure
```text
├── main.py                # Entry point (Login/Signup page)
├── pages/
│   └── dashboard.py       # Main analytics engine
├── assets/
│   └── style.css          # Custom styling & UI design
├── database.db            # SQLite user database
├── Superstore.csv         # Default dataset
├── requirements.txt       # App dependencies
└── README.md              # Project documentation