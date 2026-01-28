---

# 📈 Stock Market Data Ingestion Tool (NSE / BSE)

A **data ingestion and normalization application** built with **Python, yfinance, and Streamlit** to fetch, validate, and export Indian stock market data (NSE/BSE) in multiple granularities.

This project focuses on **data engineering concepts** such as external API ingestion, schema normalization, data validation, and controlled data delivery.

---

## 🚀 Features

* ✅ Fetch stock market data for **NSE & BSE**
* ✅ Supports **Daily, Weekly, Monthly, and Intraday** data
* ✅ Intraday intervals: **1m, 5m, 15m, 30m, 60m**
* ✅ Bulk symbol ingestion via **CSV / Excel upload**
* ✅ Manual symbol entry (comma-separated)
* ✅ Automatic handling of API limitations
* ✅ Schema normalization (`Date, Symbol, OHLC, Volume`)
* ✅ Progress tracking & failed symbol reporting
* ✅ Export data to **CSV or Excel**
* ✅ Cloud-deployable using **Streamlit**

---

## 📊 Supported Data Granularity

### Intraday Data Limits (Yahoo Finance constraint)

> ⚠️ Note: These limits are enforced automatically by the application

* **1-minute (1m)** → Last **7 days only**
* **5m / 15m / 30m / 60m** → Last **60 days only**

---

## 🧠 Data Engineering Concepts Covered

This project demonstrates real-world **data engineering responsibilities**:

* **Data Ingestion** from external APIs
* **Bulk data processing**
* **Schema validation & normalization**
* **Handling partial failures**
* **API constraint management**
* **Transformation to analytics-ready datasets**
* **Data delivery for downstream consumers**

---

## 📁 Input Format

### CSV / Excel file structure

```text
Symbol
SBIN
INFY
TCS
HDFCBANK
```

OR

### Manual input

```text
SBIN, INFY, TCS, HDFCBANK
```

---

## 📤 Output Schema

```text
Date | Symbol | Open | High | Low | Close | Volume
```

This schema is consistent across all data types (Daily & Intraday).

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit** – UI & orchestration
* **yfinance** – Market data ingestion
* **Pandas / NumPy** – Data processing
* **Yahoo Finance** – Data provider

---

## ▶️ How to Run Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deployment

This application can be deployed easily on:

* **Streamlit Community Cloud**
* **Docker + AWS / Azure / GCP**
* **Render / Railway**

---

## ⚠️ Known Limitations

* Yahoo Finance intraday data has **strict historical limits**
* NSE index intraday data may be unreliable
* This project is **data ingestion**, not price prediction

---

## 🔮 Future Enhancements (Open for Contributions)

Contributions & suggestions are **very welcome** 🙌

Possible improvements:

* 📊 Candlestick & volume charts
* 📈 Technical indicators (RSI, MACD)
* 🗄️ Database storage (PostgreSQL / BigQuery)
* ⏱️ Scheduled ingestion (Airflow / cron)
* ☁️ S3 / GCS export
* 🔐 Authentication & role-based access
* 🔌 Broker APIs (Zerodha / Upstox)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes
4. Open a Pull Request

For major changes, please open an issue first to discuss what you’d like to add.

---

## 📜 Disclaimer

This project is for **educational and analytical purposes only**.
It is **not intended for trading or financial advice**.

---

## ⭐ Feedback & Suggestions

If you find this project useful:

* ⭐ Star the repo
* 🐛 Raise an issue
* 💡 Suggest improvements

Your feedback helps improve the project!
---
