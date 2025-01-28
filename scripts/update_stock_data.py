# scripts/update_stock_data.py

import yfinance as yf
import pandas as pd
import json
from ta import trend, momentum
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period='3mo', interval='1d'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df

def calculate_indicators(df):
    # 計算 RSI
    rsi = momentum.RSIIndicator(close=df['Close'], window=14)
    df['rsi'] = rsi.rsi()

    # 計算 MACD
    macd = trend.MACD(close=df['Close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()

    return df

def prepare_json_data(df):
    data = {
        "dates": df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        "close": df['Close'].round(2).tolist(),
        "rsi": df['rsi'].round(2).tolist(),
        "macd": df['macd'].round(2).tolist(),
        "macd_signal": df['macd_signal'].round(2).tolist(),
        "macd_diff": df['macd_diff'].round(2).tolist()
    }
    return data

def main():
    # 設定股票代碼和抓取參數
    ticker = "2330.TW"  # 台積電
    period = "3mo"       # 最近三個月
    interval = "1d"      # 日線

    # 抓取數據
    df = fetch_stock_data(ticker, period, interval)

    # 計算技術指標
    df = calculate_indicators(df)

    # 準備 JSON 數據
    json_data = prepare_json_data(df)

    # 定義 JSON 文件路徑
    json_file_path = 'data/stock_data.json'

    # 寫入 JSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"股票數據已更新至 {json_file_path} (更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == "__main__":
    main()
