import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="NSE Stock Data Downloader", layout="wide")
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

start_date = st.sidebar.date_input("Start Date", date(2025, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

output_format = st.sidebar.selectbox("Output Format", ["CSV", "Excel"])
file_mode = st.sidebar.radio("File Mode", ["Single File", "Separate per Symbol"])

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel with Symbols",
    type=["csv", "xlsx"]
)

# ---------------- FETCH LOGIC ----------------
if uploaded_file and st.button("🚀 Fetch Data"):

    if uploaded_file.name.endswith(".csv"):
        symbols_df = pd.read_csv(uploaded_file)
    else:
        symbols_df = pd.read_excel(uploaded_file)

    symbols = symbols_df["Symbol"].dropna().unique()
    all_data = []
    failed_symbols = []

    progress = st.progress(0)

    for i, symbol in enumerate(symbols):
        try:
            ticker = yf.Ticker(f"{symbol}{suffix}")

            data = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval if data_type == "Intraday" else interval_map[data_type]
            )

            if not data.empty:
                data = data[["Open", "High", "Low", "Close", "Volume"]]
                data["Symbol"] = symbol
                data.reset_index(inplace=True)
                all_data.append(data)

        except Exception:
            failed_symbols.append(symbol)

        progress.progress((i + 1) / len(symbols))

    if not all_data:
        st.error("❌ No data fetched. Check symbols or date range.")
    else:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df = final_df[["Date", "Symbol", "Open", "High", "Low", "Close", "Volume"]]

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
            excel_buffer = pd.ExcelWriter("stock_data.xlsx", engine="xlsxwriter")
            final_df.to_excel(excel_buffer, index=False, sheet_name="Data")
            excel_buffer.close()

            with open("stock_data.xlsx", "rb") as f:
                st.download_button(
                    "⬇️ Download Excel",
                    f,
                    file_name="stock_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        if failed_symbols:
            st.warning(f"⚠️ Failed symbols: {', '.join(failed_symbols)}")
