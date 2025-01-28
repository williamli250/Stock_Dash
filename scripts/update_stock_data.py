# scripts/update_stock_data.py

import yfinance as yf
import pandas as pd
import json
from ta import trend, momentum
from datetime import datetime, timedelta

# 股票代碼字典
tickers = {
    '台積電': '2330.TW',
    '富邦印度': '00652.TW',
    '永豐ESG': '00930.TW',
    '聯發科': '2454.TW',
    '聯電': '2303.TW',
    '台灣大盤指數': '^TWII'
}

def fetch_stock_data(ticker, period='3mo', interval='1d'):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    df['ticker'] = ticker
    return df

def calculate_indicators(df):
    if len(df) < 14:
        df['RSI'] = None
    else:
        rsi = momentum.RSIIndicator(close=df['Close'], window=14)
        df['RSI'] = rsi.rsi()

    if len(df) < 26:
        df['MACD'] = None
        df['MACD_signal'] = None
        df['MACD_diff'] = None
    else:
        macd = trend.MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()

    if len(df) < 50:
        df['SMA'] = None
        df['EMA'] = None
    else:
        sma = trend.SMAIndicator(close=df['Close'], window=50)
        ema = trend.EMAIndicator(close=df['Close'], window=50)
        df['SMA'] = sma.sma_indicator()
        df['EMA'] = ema.ema_indicator()

    if len(df) < 20:
        df['BB High'] = None
        df['BB Low'] = None
    else:
        bollinger = trend.BollingerBands(close=df['Close'])
        df['BB High'] = bollinger.bollinger_hband()
        df['BB Low'] = bollinger.bollinger_lband()

    if len(df) < 9:
        df['K'] = None
        df['D'] = None
        df['Stochastic RSI'] = None
    else:
        stoch = momentum.StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=9, smooth_window=9)
        df['K'] = stoch.stoch()
        df['D'] = stoch.stoch_signal()
        df['Stochastic RSI'] = stoch.stoch()

    if len(df) < 14:
        df['Williams %R'] = None
    else:
        williams = momentum.WilliamsRIndicator(high=df['High'], low=df['Low'], close=df['Close'], lbp=14)
        df['Williams %R'] = williams.williams_r()

    if len(df) < 20:
        df['CCI'] = None
    else:
        cci = trend.CCIIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=20)
        df['CCI'] = cci.cci()

    if len(df) < 14:
        df['ADX'] = None
    else:
        adx = trend.ADXIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=14)
        df['ADX'] = adx.adx()

    return df

def main():
    all_data = []

    for name, ticker in tickers.items():
        print(f"Fetching data for {name} ({ticker})...")
        df = fetch_stock_data(ticker, period="3mo", interval="1d")
        df = calculate_indicators(df)
        # 選擇需要的列
        df = df[['ticker', 'Date', 'Close', 'MACD', 'MACD_signal', 'MACD_diff', 'RSI', 'SMA', 'EMA', 'BB High', 'BB Low', 'K', 'D', 'Stochastic RSI', 'CCI', 'Williams %R', 'ADX']]
        # 填充 NaN 為 null
        df = df.where(pd.notnull(df), None)
        all_data.extend(df.to_dict(orient='records'))

    # 將數據寫入 JSON 文件
    json_file_path = 'data/stock_data.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"股票數據已更新至 {json_file_path} (更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == "__main__":
    main()
