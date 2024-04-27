import os
import yfinance as yf
import pandas as pd
import datetime
import logging
import openpyxl

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_stock_data():
    excel_file_path = 'Airflow Scripts/Data/stock_info.xlsx'

    today = datetime.date.today()
    if today.weekday() >= 5:  # If it's Saturday or Sunday
        logging.info("No market data for weekends")
        return

    tickers = ["JPM", "GS", "BAC", "MS", "WFC", "C"]
    data = yf.download(tickers, start=today.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
    if data.empty:
        logging.info("No data available for today.")
        return

    if not os.path.exists(excel_file_path):
        logging.error("Excel file does not exist.")
        return

    try:
        workbook = openpyxl.load_workbook(excel_file_path)
    except Exception as e:
        logging.error(f"Failed to load the Excel workbook: {e}")
        return

    for ticker in tickers:
        if ticker in data['Close'].columns:
            ws = workbook[ticker]
            row = ws.max_row + 1
            ws.append([
                today.strftime('%Y-%m-%d'),
                ticker,
                yf.Ticker(ticker).info['longName'],
                data['Close'][ticker].iloc[0],
                data['High'][ticker].iloc[0],
                data['Low'][ticker].iloc[0],
                data['Volume'][ticker].iloc[0]
            ])

    workbook.save(excel_file_path)
    logging.info("Stock data successfully updated.")

if __name__ == "__main__":
    update_stock_data()
