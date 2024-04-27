import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import zipfile
import os


# Function to download stock data
def download_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(f'{symbol}.BO', start=start_date, end=end_date)
        stock_data['Symbol'] = symbol  # Add a new column with the symbol name
        stock_data.reset_index(inplace=True)  # Reset index to include 'Date' as a column
        return stock_data
    except Exception as e:
        st.error(f"Error downloading data for {symbol}: {e}")
        return pd.DataFrame()


# Save DataFrame to CSV and add to ZIP
def save_to_zip(data, zip_path, symbol):
    csv_path = f"{symbol}.csv"
    data.to_csv(csv_path, index=False)
    with zipfile.ZipFile(zip_path, 'a') as z:
        z.write(csv_path)
    os.remove(csv_path)  # Clean up the CSV file


# Streamlit app
def main():
    st.title('Stock Data Downloader')

    # File uploader
    uploaded_file = st.file_uploader("Upload your file with stock symbols", type=['csv'])
    if uploaded_file is not None:
        # To read file as string:
        symbols_data = pd.read_csv(uploaded_file)
        symbols = symbols_data['SYMBOL'].tolist()  # Adjust field name as necessary

        # Select date range
        start_date = st.date_input('Start date', datetime.today() - timedelta(days=365))
        end_date = st.date_input('End date', datetime.today())

        if st.button('Download and Zip Data'):
            if start_date < end_date:
                zip_path = 'stock_data.zip'
                for symbol in symbols:
                    data = download_stock_data(symbol, start_date, end_date)
                    if not data.empty:
                        save_to_zip(data, zip_path, symbol)
                st.success("Downloaded and zipped data for all symbols")
                with open(zip_path, "rb") as fp:
                    btn = st.download_button(
                        label="Download ZIP",
                        data=fp,
                        file_name=zip_path,
                        mime="application/zip"
                    )
                os.remove(zip_path)  # Clean up the ZIP file
            else:
                st.error('End date must be after start date.')


if __name__ == '__main__':
    main()
