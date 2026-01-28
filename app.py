import streamlit as st
import yfinance as yf
import pandas as pd
import logging
from datetime import date, timedelta

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Stock Data Downloader", layout="wide")
st.title("📈 NSE / BSE Stock Data Downloader")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Configuration")

exchange = st.sidebar.selectbox("Select Exchange", ["NSE", "BSE"])
suffix = ".NS" if exchange == "NSE" else ".BO"

data_type = st.sidebar.selectbox(
    "Data Type",
    ["Daily", "Weekly", "Monthly", "Intraday"]
)

interval_map = {
    "Daily": "1d",
    "Weekly": "1wk",
    "Monthly": "1mo"
}

interval = "1d"
if data_type == "Intraday":
    interval = st.sidebar.selectbox(
        "Intraday Interval",
        ["1m", "5m", "15m", "30m", "60m"]
    )

start_date = st.sidebar.date_input(
    "Start Date", date.today() - timedelta(days=30)
)
end_date = st.sidebar.date_input("End Date", date.today())

output_format = st.sidebar.selectbox("Output Format", ["CSV", "Excel"])

# ---------------- INTRADAY NOTE ----------------
if data_type == "Intraday":
    st.info(
        "ℹ️ **Intraday Data Limitation (Yahoo Finance)**\n\n"
        "- **1m interval** → last **7 days only**\n"
        "- **5m / 15m / 30m / 60m** → last **60 days only**\n"
        "- Date range will be **auto-adjusted automatically**"
    )

# ---------------- SYMBOL INPUT ----------------
st.subheader("📌 Stock Symbols")

input_mode = st.radio(
    "Choose symbol input method",
    ["Upload CSV / Excel", "Enter symbols manually"]
)

symbols = []

if input_mode == "Upload CSV / Excel":
    uploaded_file = st.file_uploader(
        "Upload file (must contain `Symbol` column)",
        type=["csv", "xlsx"]
    )

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        symbols = df["Symbol"].dropna().astype(str).unique().tolist()

else:
    symbol_text = st.text_input(
        "Enter symbols (comma-separated)",
        placeholder="SBIN, INFY, TCS, HDFCBANK"
    )

    if symbol_text:
        symbols = [s.strip().upper() for s in symbol_text.split(",") if s.strip()]

# ---------------- FETCH BUTTON (ONLY ONCE) ----------------
fetch_clicked = st.button("🚀 Fetch Data")

# ---------------- FETCH LOGIC ----------------
if fetch_clicked:
    if not symbols:
        st.warning("Please upload a file or enter at least one symbol.")
        st.stop()

    all_data = []
    failed_symbols = []

    # ---- Intraday date enforcement ----
    if data_type == "Intraday":
        max_days = 7 if interval == "1m" else 60
        allowed_start = end_date - timedelta(days=max_days)

        if start_date < allowed_start:
            st.warning(
                f"⚠️ Start date adjusted to last {max_days} days "
                f"due to intraday limits."
            )
            start_date = allowed_start

    progress = st.progress(0.0)

    for i, symbol in enumerate(symbols):
        try:
            ticker = yf.Ticker(f"{symbol}{suffix}")

            data = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval if data_type == "Intraday" else interval_map[data_type],
                auto_adjust=False,
                prepost=False
            )

            if not data.empty:
                data = data[["Open", "High", "Low", "Close", "Volume"]]
                data["Symbol"] = symbol
                data.reset_index(inplace=True)

                # ---- Fix Date vs Datetime ----
                if "Datetime" in data.columns:
                    data.rename(columns={"Datetime": "Date"}, inplace=True)

                all_data.append(data)
            else:
                failed_symbols.append(symbol)

        except Exception as e:
            logger.error(f"{symbol} failed: {e}")
            failed_symbols.append(symbol)

        progress.progress((i + 1) / len(symbols))

    # ---------------- FINAL DATAFRAME ----------------
    if not all_data:
        st.error("❌ No data fetched. Check symbols or date range.")
        st.stop()

    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df[
        ["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]
    ]

    # ---------------- EXCEL TIMEZONE FIX ----------------
    if pd.api.types.is_datetime64_any_dtype(final_df["Date"]):
        final_df["Date"] = final_df["Date"].dt.tz_localize(None)

    st.success("✅ Data fetched successfully")
    st.dataframe(final_df, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    if output_format == "CSV":
        csv = final_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            csv,
            file_name="stock_data.csv",
            mime="text/csv"
        )
    else:
        with pd.ExcelWriter("stock_data.xlsx", engine="xlsxwriter") as writer:
            final_df.to_excel(writer, index=False, sheet_name="Data")

        with open("stock_data.xlsx", "rb") as f:
            st.download_button(
                "⬇️ Download Excel",
                f,
                file_name="stock_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    if failed_symbols:
        st.warning(f"⚠️ Failed symbols: {', '.join(failed_symbols)}")
