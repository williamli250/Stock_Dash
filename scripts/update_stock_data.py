# scripts/update_stock_data.py

import os
import yfinance as yf
import pandas as pd
import json
from ta import trend, momentum, volatility
from datetime import datetime

# 股票代碼字典
tickers = {
    '台積電': '2330.TW',
    '富邦印度': '00652.TW',
    '永豐ESG': '00930.TW',
    '聯發科': '2454.TW',
    '元大美債': '00679B.TWO',  # 正確代碼
    '台灣大盤指數': '^TWII'
}

def fetch_stock_data(ticker, period='2y', interval='1d'):
    """
    抓取股票歷史數據。

    :param ticker: 股票代碼
    :param period: 時間範圍（如 "2y" 表示兩年）
    :param interval: 數據間隔（如 "1d" 表示日線）
    :return: 包含歷史數據的 DataFrame
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        if df.empty:
            print(f"警告：沒有找到 {ticker} 的數據。")
            return pd.DataFrame()  # 返回空的 DataFrame
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])  # 確保 Date 欄位為 datetime 格式
        df['ticker'] = ticker
        return df
    except Exception as e:
        print(f"錯誤：抓取 {ticker} 的數據時發生錯誤：{e}")
        return pd.DataFrame()

def calculate_indicators(df):
    """
    計算技術指標並將其添加到 DataFrame 中。

    :param df: 包含歷史數據的 DataFrame
    :return: 包含技術指標的 DataFrame
    """
    # RSI
    if len(df) >= 14:
        rsi = momentum.RSIIndicator(close=df['Close'], window=14)
        df['RSI'] = rsi.rsi()
    else:
        df['RSI'] = None

    # MACD
    if len(df) >= 26:
        macd = trend.MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()
    else:
        df['MACD'] = None
        df['MACD_signal'] = None
        df['MACD_diff'] = None

    # SMA 和 EMA
    if len(df) >= 50:
        sma = trend.SMAIndicator(close=df['Close'], window=50)
        ema = trend.EMAIndicator(close=df['Close'], window=50)
        df['SMA'] = sma.sma_indicator()
        df['EMA'] = ema.ema_indicator()
    else:
        df['SMA'] = None
        df['EMA'] = None

    # 布林帶
    if len(df) >= 20:
        bollinger = volatility.BollingerBands(close=df['Close'])
        df['BB High'] = bollinger.bollinger_hband()
        df['BB Low'] = bollinger.bollinger_lband()
    else:
        df['BB High'] = None
        df['BB Low'] = None

    # 隨機指標 K 和 D
    if len(df) >= 14:
        stoch = momentum.StochasticOscillator(
            high=df['High'], 
            low=df['Low'], 
            close=df['Close'], 
            window=14, 
            smooth_window=3
        )
        df['K'] = stoch.stoch()
        df['D'] = stoch.stoch_signal()
    else:
        df['K'] = None
        df['D'] = None

    # Stochastic RSI
    if len(df) >= 14:
        stoch_rsi = momentum.StochRSIIndicator(
            close=df['Close'], 
            window=14, 
            smooth1=3, 
            smooth2=3
        )
        df['Stochastic RSI'] = stoch_rsi.stochrsi()
    else:
        df['Stochastic RSI'] = None

    # Williams %R
    if len(df) >= 14:
        williams = momentum.WilliamsRIndicator(
            high=df['High'], 
            low=df['Low'], 
            close=df['Close'], 
            lbp=14
        )
        df['Williams %R'] = williams.williams_r()
    else:
        df['Williams %R'] = None

    # CCI
    if len(df) >= 20:
        cci = trend.CCIIndicator(
            high=df['High'], 
            low=df['Low'], 
            close=df['Close'], 
            window=20
        )
        df['CCI'] = cci.cci()
    else:
        df['CCI'] = None

    # ADX
    if len(df) >= 14:
        adx = trend.ADXIndicator(
            high=df['High'], 
            low=df['Low'], 
            close=df['Close'], 
            window=14
        )
        df['ADX'] = adx.adx()
    else:
        df['ADX'] = None

    return df

def main():
    all_data = []

    # 獲取腳本所在的目錄
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 構建 stock_data.json 的絕對路徑
    json_file_path = os.path.join(script_dir, '..', 'data', 'stock_data.json')

    for name, ticker in tickers.items():
        print(f"Fetching data for {name} ({ticker})...")
        df = fetch_stock_data(ticker, period="2y", interval="1d")
        if df.empty:
            print(f"跳過 {name} ({ticker})，因為沒有數據。")
            continue  # 如果沒有數據，跳過

        df = calculate_indicators(df)
        # 選擇需要的列
        required_columns = [
            'ticker', 'Date', 'Close', 'MACD', 'MACD_signal', 'MACD_diff', 
            'RSI', 'SMA', 'EMA', 'BB High', 'BB Low', 'K', 'D', 
            'Stochastic RSI', 'CCI', 'Williams %R', 'ADX'
        ]
        # 確保所有必需的列都存在
        existing_columns = [col for col in required_columns if col in df.columns]
        df = df[existing_columns]
        # 將 'Date' 欄位轉換為字符串格式
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        # 移除含有任何 NaN 值的行
        df.dropna(inplace=True)
        # 填充 NaN 為 null（僅針對仍然存在的 NaN）
        df = df.where(pd.notnull(df), None)
        all_data.extend(df.to_dict(orient='records'))

    if not all_data:
        print("沒有數據需要寫入。")
        return

    # 確保 data 目錄存在
    data_dir = os.path.dirname(json_file_path)
    os.makedirs(data_dir, exist_ok=True)

    # 將數據寫入 JSON 文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"股票數據已更新至 {json_file_path} (更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

if __name__ == "__main__":
    main()