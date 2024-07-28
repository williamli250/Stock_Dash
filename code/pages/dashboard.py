from dash import html, dcc, dash_table
from app import app
import dash_bootstrap_components as dbc
import yfinance as yf
import pandas as pd
import ta
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

# 技術指標的附註信息
TOOLTIPS = {
    "MACD": "MACD (Moving Average Convergence Divergence): 用於識別價格趨勢和轉變信號。",
    "RSI": "RSI (Relative Strength Index): 衡量價格變動的速度和變動幅度，用於判斷股票是否處於超買或超賣狀態。",
    "SMA": "SMA (Simple Moving Average): 簡單移動平均線，用於識別價格趨勢。",
    "EMA": "EMA (Exponential Moving Average): 指數移動平均線，對近期價格變動更敏感。",
    "BB High": "BB High (布林帶上軌): 用於判斷價格的超買狀態。",
    "BB Low": "BB Low (布林帶下軌): 用於判斷價格的超賣狀態。",
    "Stochastic RSI": "Stochastic RSI: 結合隨機指標和相對強弱指標，用於識別超買和超賣狀態。",
    "CCI": "CCI (Commodity Channel Index): 用於識別價格的超買和超賣狀態。",
    "K": "K (Stochastic Oscillator): 用於判斷市場的超買或超賣狀態。",
    "D": "D (Stochastic Oscillator): 用於判斷市場的超買或超賣狀態。",
    "Williams %R": "Williams %R: 用於識別超買和超賣狀態。",
    "ADX": "ADX (Average Directional Index): 用於測量趨勢的強度。",
    "Close Price": "收盤價: 當天交易結束時的最後價格，用於判斷當日的市場情況。"
}

# 顯示名稱和列名的映射
INDICATOR_MAPPING = {
    "MACD": "MACD",
    "RSI": "RSI",
    "SMA": "SMA",
    "EMA": "EMA",
    "BB High": "BB_high",
    "BB Low": "BB_low",
    "Stochastic RSI": "Stochastic RSI",
    "CCI": "CCI",
    "K": "K",
    "D": "D",
    "Williams %R": "Williams %R",
    "ADX": "ADX",
    "Close Price": "Close"
}

def get_stock_data(ticker, interval):
    end_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    df.reset_index(inplace=True)
    
    # 檢查是否有 'Date' 列，否則改用 'Datetime'
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    elif 'Datetime' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)
    else:
        raise ValueError("Data does not contain 'Date' or 'Datetime' columns")
    
    return df

def add_technical_indicators(df):
    if len(df) < 15:  # 確保有足夠的數據來計算技術指標
        raise ValueError("Not enough data to calculate technical indicators")
    
    df['MACD'] = ta.trend.MACD(df['Close']).macd()
    df['MACD_signal'] = ta.trend.MACD(df['Close']).macd_signal()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['SMA'] = ta.trend.SMAIndicator(df['Close'], window=14).sma_indicator()
    df['EMA'] = ta.trend.EMAIndicator(df['Close'], window=14).ema_indicator()
    bollinger = ta.volatility.BollingerBands(df['Close'])
    df['BB_high'] = bollinger.bollinger_hband()
    df['BB_low'] = bollinger.bollinger_lband()
    df['Stochastic RSI'] = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close']).stoch()
    df['K'] = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close']).stoch()
    df['D'] = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close']).stoch_signal()
    df['Williams %R'] = ta.momentum.WilliamsRIndicator(df['High'], df['Low'], df['Close']).williams_r()
    df['CCI'] = ta.trend.CCIIndicator(df['High'], df['Low'], df['Close']).cci()
    df['ADX'] = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close']).adx()
    return df

def evaluate_signals(df):
    latest_data = df.iloc[-1]
    macd = latest_data['MACD']
    macd_signal = latest_data['MACD_signal']
    rsi = latest_data['RSI']
    sma = df['SMA'].iloc[-1]
    ema = df['EMA'].iloc[-1]
    bb_high = df['BB_high'].iloc[-1]
    bb_low = df['BB_low'].iloc[-1]
    stochastic_rsi = df['Stochastic RSI'].iloc[-1]
    cci = df['CCI'].iloc[-1]
    k = df['K'].iloc[-1]
    d = df['D'].iloc[-1]
    williams_r = df['Williams %R'].iloc[-1]
    adx = df['ADX'].iloc[-1]
    close_price = df['Close'].iloc[-1]
    
    buy_signals = []
    sell_signals = []
    
    # MACD Buy/Sell Signal
    status_macd = "Wait"
    secondary_status_macd = "Wait"
    if macd > macd_signal:
        status_macd = "Buy"
        secondary_status_macd = "Buy"
        buy_signals.append("MACD > Signal (Buy)")
    if macd < macd_signal:
        status_macd = "Sell"
        secondary_status_macd = "Sell"
        sell_signals.append("MACD < Signal (Sell)")
    
    # RSI Buy/Sell Signal
    status_rsi = "Wait"
    secondary_status_rsi = "Wait"
    if rsi < 30:
        status_rsi = "Buy"
        buy_signals.append("RSI < 30 (Buy)")
    if rsi < 40:
        secondary_status_rsi = "Buy"
        buy_signals.append("RSI < 40 (Secondary Buy)")
    if rsi > 70:
        status_rsi = "Sell"
        sell_signals.append("RSI > 70 (Sell)")
    if rsi > 60:
        secondary_status_rsi = "Sell"
        sell_signals.append("RSI > 60 (Secondary Sell)")
    
    # SMA Buy/Sell Signal
    status_sma = "Wait"
    secondary_status_sma = "Wait"
    if df['Close'].iloc[-1] < sma:
        status_sma = "Buy"
        secondary_status_sma = "Buy"
    if df['Close'].iloc[-1] > sma:
        status_sma = "Sell"
        secondary_status_sma = "Sell"
    
    # EMA Buy/Sell Signal
    status_ema = "Wait"
    secondary_status_ema = "Wait"
    if df['Close'].iloc[-1] < ema:
        status_ema = "Buy"
        secondary_status_ema = "Buy"
    if df['Close'].iloc[-1] > ema:
        status_ema = "Sell"
        secondary_status_ema = "Sell"
    
    # Bollinger Bands Buy/Sell Signal
    status_bb = "Wait"
    secondary_status_bb = "Wait"
    if df['Close'].iloc[-1] < bb_low:
        status_bb = "Buy"
        buy_signals.append("Close < BB Low (Buy)")
    if df['Close'].iloc[-1] < (bb_low + (bb_high - bb_low) / 10):
        secondary_status_bb = "Buy"
        buy_signals.append("Close near BB Low (Secondary Buy)")
    if df['Close'].iloc[-1] > bb_high:
        status_bb = "Sell"
        sell_signals.append("Close > BB High (Sell)")
    if df['Close'].iloc[-1] > (bb_high - (bb_high - bb_low) / 10):
        secondary_status_bb = "Sell"
        sell_signals.append("Close near BB High (Secondary Sell)")
    
    # Stochastic RSI Buy/Sell Signal
    status_stochastic_rsi = "Wait"
    secondary_status_stochastic_rsi = "Wait"
    if stochastic_rsi < 20:
        status_stochastic_rsi = "Buy"
        buy_signals.append("Stochastic RSI < 20 (Buy)")
    if stochastic_rsi < 40:
        secondary_status_stochastic_rsi = "Buy"
        buy_signals.append("Stochastic RSI < 40 (Secondary Buy)")
    if stochastic_rsi > 80:
        status_stochastic_rsi = "Sell"
        sell_signals.append("Stochastic RSI > 80 (Sell)")
    if stochastic_rsi > 60:
        secondary_status_stochastic_rsi = "Sell"
        sell_signals.append("Stochastic RSI > 60 (Secondary Sell)")
    
    # CCI Buy/Sell Signal
    status_cci = "Wait"
    secondary_status_cci = "Wait"
    if cci < -100:
        status_cci = "Buy"
        buy_signals.append("CCI < -100 (Buy)")
    if cci < -90:
        secondary_status_cci = "Buy"
        buy_signals.append("CCI < -90 (Secondary Buy)")
    if cci > 100:
        status_cci = "Sell"
        sell_signals.append("CCI > 100 (Sell)")
    if cci > 90:
        secondary_status_cci = "Sell"
        sell_signals.append("CCI > 90 (Secondary Sell)")
    
    # K 和 D Buy/Sell Signal
    status_kd = "Wait"
    secondary_status_kd = "Wait"
    if k < 20 and d < 20 and k > d:
        status_kd = "Buy"
        buy_signals.append("K < 20 and D < 20 and K > D (Buy)")
    if k < 30 and d < 30 and k > d:
        secondary_status_kd = "Buy"
        buy_signals.append("K < 30 and D < 30 and K > D (Secondary Buy)")
    if k > 80 and d > 80 and k < d:
        status_kd = "Sell"
        sell_signals.append("K > 80 and D > 80 and K < D (Sell)")
    if k > 70 and d > 70 and k < d:
        secondary_status_kd = "Sell"
        sell_signals.append("K > 70 and D > 70 and K < D (Secondary Sell)")

    # Williams %R Buy/Sell Signal
    status_williams_r = "Wait"
    secondary_status_williams_r = "Wait"
    if williams_r < -80:
        status_williams_r = "Buy"
        buy_signals.append("Williams %R < -80 (Buy)")
    if williams_r < -60:
        secondary_status_williams_r = "Buy"
        buy_signals.append("Williams %R < -60 (Secondary Buy)")
    if williams_r > -20:
        status_williams_r = "Sell"
        sell_signals.append("Williams %R > -20 (Sell)")
    if williams_r > -40:
        secondary_status_williams_r = "Sell"
        sell_signals.append("Williams %R > -40 (Secondary Sell)")
    
    # ADX Buy/Sell Signal
    status_adx = "--"
    secondary_status_adx = "--"
    if adx > 25:
        status_adx = "Hot Trend"
        buy_signals.append("ADX > 25 (Buy)")
    if adx < 20:
        status_adx = "No Trend"
        sell_signals.append("ADX < 20 (Sell)")

    indicator_values = [
        {"Indicator": "MACD", "Value": f"{macd:.2f}", "Sell Signal": "< MACD Signal", "Buy Signal": "> MACD Signal", "Secondary Sell Signal": "< MACD Signal", "Secondary Buy Signal": "> MACD Signal", "Status": status_macd, "Secondary Status": secondary_status_macd},
        {"Indicator": "RSI", "Value": f"{rsi:.2f}", "Sell Signal": "> 70", "Buy Signal": "< 30", "Secondary Sell Signal": "> 60", "Secondary Buy Signal": "< 40", "Status": status_rsi, "Secondary Status": secondary_status_rsi},
        {"Indicator": "SMA", "Value": f"{sma:.2f}", "Sell Signal": "< Close", "Buy Signal": "> Close", "Secondary Sell Signal": "< Close", "Secondary Buy Signal": "> Close", "Status": status_sma, "Secondary Status": secondary_status_sma},
        {"Indicator": "EMA", "Value": f"{ema:.2f}", "Sell Signal": "< Close", "Buy Signal": "> Close", "Secondary Sell Signal": "< Close", "Secondary Buy Signal": "> Close", "Status": status_ema, "Secondary Status": secondary_status_ema},
        {"Indicator": "BB High", "Value": f"{bb_high:.2f}", "Sell Signal": "> Close", "Buy Signal": "-", "Secondary Sell Signal": "Near High", "Secondary Buy Signal": "-", "Status": status_bb, "Secondary Status": secondary_status_bb},
        {"Indicator": "BB Low", "Value": f"{bb_low:.2f}", "Sell Signal": "-", "Buy Signal": "< Close", "Secondary Sell Signal": "-", "Secondary Buy Signal": "Near Low", "Status": status_bb, "Secondary Status": secondary_status_bb},
        {"Indicator": "K", "Value": f"{k:.2f}", "Sell Signal": "> 80", "Buy Signal": "< 20", "Secondary Sell Signal": "> 70", "Secondary Buy Signal": "< 30", "Status": status_kd, "Secondary Status": secondary_status_kd},
        {"Indicator": "D", "Value": f"{d:.2f}", "Sell Signal": "> 80", "Buy Signal": "< 20", "Secondary Sell Signal": "> 70", "Secondary Buy Signal": "< 30", "Status": status_kd, "Secondary Status": secondary_status_kd},
        {"Indicator": "Stochastic RSI", "Value": f"{stochastic_rsi:.2f}", "Sell Signal": "> 80", "Buy Signal": "< 20", "Secondary Sell Signal": "> 60", "Secondary Buy Signal": "< 40", "Status": status_stochastic_rsi, "Secondary Status": secondary_status_stochastic_rsi},
        {"Indicator": "CCI", "Value": f"{cci:.2f}", "Sell Signal": "> 100", "Buy Signal": "< -100", "Secondary Sell Signal": "> 90", "Secondary Buy Signal": "< -90", "Status": status_cci, "Secondary Status": secondary_status_cci},
        {"Indicator": "Williams %R", "Value": f"{williams_r:.2f}", "Sell Signal": "> -20", "Buy Signal": "< -80", "Secondary Sell Signal": "> -40", "Secondary Buy Signal": "< -60", "Status": status_williams_r, "Secondary Status": secondary_status_williams_r},
        {"Indicator": "ADX", "Value": f"{adx:.2f}", "Sell Signal": "< 20", "Buy Signal": "> 25", "Secondary Sell Signal": "--", "Secondary Buy Signal": "--", "Status": status_adx, "Secondary Status": "--"},
        {"Indicator": "Close Price", "Value": f"{close_price:.2f}", "Sell Signal": "-", "Buy Signal": "-", "Secondary Sell Signal": "-", "Secondary Buy Signal": "-", "Status": "-", "Secondary Status": "-"}
    ]
    
    return latest_data, buy_signals, sell_signals, indicator_values

tickers = {
    '台積電': '2330.TW',
    '富邦印度': '00652.TW',
    '永豐ESG': '00930.TW',
    '聯發科': '2454.TW',
    '聯電': '2303.TW',
    '台灣大盤指數': '^TWII'
}

indicators_options = [
    {"label": "MACD (Moving Average Convergence Divergence)", "value": "MACD"},
    {"label": "RSI (Relative Strength Index)", "value": "RSI"},
    {"label": "SMA (Simple Moving Average)", "value": "SMA"},
    {"label": "EMA (Exponential Moving Average)", "value": "EMA"},
    {"label": "BB High (布林帶上軌)", "value": "BB High"},
    {"label": "BB Low (布林帶下軌)", "value": "BB Low"},
    {"label": "K (Stochastic Oscillator)", "value": "K"},
    {"label": "D (Stochastic Oscillator)", "value": "D"},
    {"label": "Stochastic RSI", "value": "Stochastic RSI"},
    {"label": "CCI (Commodity Channel Index)", "value": "CCI"},
    {"label": "Williams %R", "value": "Williams %R"},
    {"label": "ADX (Average Directional Index)", "value": "ADX"},
    {"label": "Close Price", "value": "Close Price"}
]

layout = dbc.Container([
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
    dbc.Row([
        dbc.Col(html.A(html.Button("回首頁", className="btn btn-primary", style={'float': 'right'}), href="/"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H1("Stock Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row(id='today-status'),


    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='interval-selection',
            options=[
                {"label": "60分鐘線", "value": "60m"},
                {"label": "日線", "value": "1d"},
                {"label": "週線", "value": "1wk"},
            ],
            value='1d',  # 設置日線為初始值
            className="mb-3",
            style={'backgroundColor': '#333333', 'color': 'white'}
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='stock-ticker',
            options=[{'label': name, 'value': ticker} for name, ticker in tickers.items()],
            value='2330.TW',
            className="mb-3",
            style={'backgroundColor': '#333333', 'color': 'white'}
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='indicator-selection',
            options=indicators_options,
            multi=True,
            value=["RSI"],  # 預設值為 "RSI"
            className="mb-3",
            style={'backgroundColor': '#333333', 'color': 'white'}
        ), width=6)
    ], style={'backgroundColor': 'black'}),

    dbc.Row(dbc.Col(dash_table.DataTable(
        id='indicators-table',
        columns=[
            {"name": "Indicator", "id": "Indicator"},
            {"name": "Value", "id": "Value"},
            {"name": "Sell Signal", "id": "Sell Signal"},
            {"name": "Buy Signal", "id": "Buy Signal"},
            {"name": "Secondary Sell Signal", "id": "Secondary Sell Signal"},
            {"name": "Secondary Buy Signal", "id": "Secondary Buy Signal"},
            {"name": "Status", "id": "Status"},
            {"name": "Secondary Status", "id": "Secondary Status"}
        ],
        style_data_conditional=[
            {
                'if': {'column_id': 'Indicator', 'filter_query': '{Indicator} = "MACD" || {Indicator} = "RSI"'},
                'backgroundColor': 'rgba(255, 255, 0, 0.4)',
                'color': 'white'
            },
            {
                'if': {'column_id': 'Indicator', 'filter_query': '{Indicator} = "SMA" || {Indicator} = "EMA"'},
                'backgroundColor': 'rgba(135, 206, 235, 0.35)',
                'color': 'white'
            },
            {
                'if': {'column_id': 'Indicator', 'filter_query': '{Indicator} = "BB High" || {Indicator} = "BB Low" || {Indicator} = "K" || {Indicator} = "D"'},
                'backgroundColor': 'rgba(144, 238, 144, 0.3)',  
                'color': 'white'
            }, 
            {
                'if': {'column_id': 'Indicator', 'filter_query': '{Indicator} = "Stochastic RSI" || {Indicator} = "CCI" || {Indicator} = "Williams %R"'},
                'backgroundColor': 'rgba(255, 165, 0, 0.3)',
                'color': 'white'
            },
            {
                'if': {'column_id': 'Indicator', 'filter_query': '{Indicator} = "ADX" || {Indicator} = "Close Price"'},
                'backgroundColor': 'rgba(255, 192, 203, 0.4)',  
                'color': 'white'
            },
            {
                'if': {'filter_query': '{Status} = "Buy"', 'column_id': 'Status'},
                'backgroundColor': 'rgba(0, 255, 0, 0.5)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Status} = "Sell"', 'column_id': 'Status'},
                'backgroundColor': 'rgba(255, 0, 0, 0.6)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Secondary Status} = "Buy"', 'column_id': 'Secondary Status'},
                'backgroundColor': 'rgba(0, 255, 0, 0.5)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Secondary Status} = "Sell"', 'column_id': 'Secondary Status'},
                'backgroundColor': 'rgba(255, 0, 0, 0.6)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Status} = "Wait"', 'column_id': 'Status'},
                'backgroundColor': 'rgba(255, 255, 0, 0.5)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Secondary Status} = "Wait"', 'column_id': 'Secondary Status'},
                'backgroundColor': 'rgba(255, 255, 0, 0.5)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Status} = "Hot Trend"', 'column_id': 'Status'},
                'backgroundColor': 'rgba(255, 192, 203, 0.55)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            {
                'if': {'filter_query': '{Status} = "No Trend"', 'column_id': 'Status'},
                'backgroundColor': 'rgba(255, 192, 203, 0.3)',
                'color': 'white',
                'fontWeight': 'bold'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(50, 50, 50)',
            'fontWeight': 'bold',
            'color': 'white'
        },
        style_cell={
            'textAlign': 'center',
            'height': 'auto',
            'whiteSpace': 'normal',
            'backgroundColor': 'black',
            'color': 'white'
        },
        style_table={'overflowX': 'auto'}
    ), width=12)),
    dbc.Row([
        dbc.Col(dcc.Graph(id='price-chart', config={'displayModeBar': False}), width=6),
        dbc.Col(dcc.Graph(id='indicator-chart', config={'displayModeBar': False}), width=6)
    ], style={'backgroundColor': 'black'}),
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行
], fluid=True, style={'backgroundColor': 'black'})

def get_today_status(tickers):
    statuses = []
    for name, ticker in tickers.items():
        end_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')  # 確保涵蓋今天的數據
        df = yf.download(ticker, start=start_date, end=end_date, interval='1d')
        
        if df.empty or len(df) < 2:
            status = html.Div([
                html.P(f"{name}", style={'color': 'white', 'marginBottom': '5px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                html.P("No data available", style={'color': 'white'})
            ], className="stock-status")
        else:
            latest_close = df['Close'].iloc[-1]
            previous_close = df['Close'].iloc[-2]
            change = latest_close - previous_close
            change_percent = (change / previous_close) * 100
            
            if change > 0:
                color = 'lightcoral'  # 淡紅色
                change_text = f"↑ {change_percent:.2f}%"
            elif change < 0:
                color = 'lightgreen'  # 淡綠色
                change_text = f"↓ {-change_percent:.2f}%"
            else:
                color = 'white'
                change_text = f"{change_percent:.2f}%"
            
            status = html.Div([
                html.P(f"{name}", style={'color': 'white', 'marginBottom': '5px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                html.P(f"股價: ${latest_close:.2f}", style={'color': 'white'}),
                html.P(change_text, style={'color': color})
            ], className="stock-status")
        
        statuses.append(status)
    
    return statuses

@app.callback(
    [Output('price-chart', 'figure'), Output('indicator-chart', 'figure'), Output('indicators-table', 'data'), Output('today-status', 'children')],
    [Input('stock-ticker', 'value'), Input('indicator-selection', 'value'), Input('interval-selection', 'value')]
)
def update_charts(ticker, selected_indicators, interval):
    df = get_stock_data(ticker, interval)
    try:
        df = add_technical_indicators(df)
    except ValueError as e:
        return go.Figure(), go.Figure(), [], html.Div("Data is not sufficient to display indicators", style={'color': 'red', 'textAlign': 'center'})
    
    latest_data, buy_signals, sell_signals, indicator_values = evaluate_signals(df)
    
    # 獲取今日狀況
    today_status_elements = get_today_status(tickers)
    today_status = dbc.Row([
        dbc.Col(today_status_elements[i], width=2, style={'padding': '5px'}) for i in range(len(today_status_elements))
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'backgroundColor': '#333333', 'padding': '10px', 'borderRadius': '5px'})

    price_fig = go.Figure()
    price_fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name='Price'
    ))
    price_fig.update_layout(
        title=f"{ticker} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        template='plotly_dark',
        paper_bgcolor='rgba(0, 0, 0, 0.5)',  # 圖表外部背景顏色
        plot_bgcolor='rgba(0, 0, 0, 0.5)',  # 圖表內部背景顏色
        font=dict(color='white'),  # 字體顏色
        hovermode='x unified'  # 設定 hovermode 為 x unified
    )
    
    indicator_fig = go.Figure()
    if 'MACD' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'))
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name='MACD Signal'))
    if 'RSI' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[70], mode='markers+text', name='Sell Signal', text=['70'], textposition='top center'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[30], mode='markers+text', name='Buy Signal', text=['30'], textposition='top center'))
    if 'SMA' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], name='SMA'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[latest_data['Close']], mode='markers+text', name='SMA Signal', text=[f"Close: {latest_data['Close']}"], textposition='top center'))
    if 'EMA' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], name='EMA'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[latest_data['Close']], mode='markers+text', name='EMA Signal', text=[f"Close: {latest_data['Close']}"], textposition='top center'))
    if 'BB High' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['BB_high'], name='BB High'))
    if 'BB Low' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['BB_low'], name='BB Low'))
    if 'K' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['K'], name='K'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[80], mode='markers+text', name='Sell Signal', text=['80'], textposition='top center'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[20], mode='markers+text', name='Buy Signal', text=['20'], textposition='top center'))
    if 'D' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['D'], name='D'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[80], mode='markers+text', name='Sell Signal', text=['80'], textposition='top center'))
        indicator_fig.add_trace(go.Scatter(x=[df.index[-1]], y=[20], mode='markers+text', name='Buy Signal', text=['20'], textposition='top center'))
    if 'Stochastic RSI' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['Stochastic RSI'], name='Stochastic RSI'))
    if 'CCI' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['CCI'], name='CCI'))
    if 'Williams %R' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['Williams %R'], name='Williams %R'))
    if 'ADX' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['ADX'], name='ADX'))
    if 'Close Price' in selected_indicators:
        indicator_fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price'))
    
    indicator_fig.update_layout(
        title="Technical Indicators",
        xaxis_title="Date",
        yaxis_title="Value",
        template='plotly_dark',
        xaxis_rangeslider_visible=True,
        paper_bgcolor='rgba(0, 0, 0, 0.5)',  # 圖表外部背景顏色
        plot_bgcolor='rgba(0, 0, 0, 0.5)',  # 圖表內部背景顏色
        font=dict(color='white'),  # 字體顏色
        hovermode='x unified'  # 設定 hovermode 為 x unified
    )
    
    return price_fig, indicator_fig, indicator_values, today_status