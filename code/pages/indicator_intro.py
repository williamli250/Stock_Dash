from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

layout = dbc.Container([
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行

    dbc.Row([
        dbc.Col(
            dbc.Button("回首頁", href="/", color="primary", className="mt-4", style={'float': 'right'}),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(html.H1("Indicator Introduction", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dbc.ButtonGroup(
                [
                    dbc.Button("指標介紹", id="btn-indicator-intro", n_clicks=1, className="btn-modern btn-modern-primary"),  # 默認 n_clicks 為 1
                    dbc.Button("組合策略", id="btn-combo-strategy", n_clicks=0, className="btn-modern btn-modern-secondary")
                ], 
                className="mb-4 d-flex justify-content-center"  # 添加 className 属性以置中
            ),
            width=12,
            className="d-flex justify-content-center"
        )
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='indicator-content'), width=12)
    ]),
], fluid=True)

@app.callback(
    [Output('btn-indicator-intro', 'className'),
     Output('btn-combo-strategy', 'className'),
     Output('indicator-content', 'children')],
    [Input('btn-indicator-intro', 'n_clicks'),
     Input('btn-combo-strategy', 'n_clicks')]
)
def display_content(btn_indicator_intro, btn_combo_strategy):
    ctx = callback_context

    if not ctx.triggered:
        button_id = 'btn-indicator-intro'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "btn-indicator-intro":
        return 'btn-modern btn-modern-primary', 'btn-modern btn-modern-secondary', [
            dbc.Row([
                dbc.Col(html.H3("MACD (Moving Average Convergence Divergence)"), width=12),
                dbc.Col(html.P("用途：MACD 用於識別價格趨勢和轉變信號。它通過計算短期和長期的移動平均線之間的差異來判斷市場的走勢。當MACD線上穿信號線時，通常被視為買入信號；反之，當MACD線下穿信號線時，通常被視為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("RSI (Relative Strength Index)"), width=12),
                dbc.Col(html.P("用途：RSI 用於衡量價格變動的速度和變動幅度，以判斷股票是否處於超買或超賣狀態。通常，RSI值超過70表示股票超買，可能面臨回調；RSI值低於30表示股票超賣，可能會反彈。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("SMA (Simple Moving Average)"), width=12),
                dbc.Col(html.P("用途：SMA 是簡單移動平均線，用於識別價格趨勢。它是某一特定期間內價格的平均值，有助於平滑價格數據，幫助投資者判斷長期趨勢。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("EMA (Exponential Moving Average)"), width=12),
                dbc.Col(html.P("用途：EMA 是指數移動平均線，相較於SMA對近期價格變動更敏感。EMA 能夠更快地反映最新的價格變動，適合用於短期交易決策。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("BB (Bollinger Bands)"), width=12),
                dbc.Col(html.P("用途：布林帶由三條線組成：中間的移動平均線以及上下的價格波動範圍。BB上軌（BB High）用於判斷價格的超買狀態，而BB下軌（BB Low）用於判斷價格的超賣狀態。當價格接近上軌時，可能表示市場過熱；當價格接近下軌時，可能表示市場超賣。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("K (Stochastic Oscillator)"), width=12),
                dbc.Col(html.P("用途：隨機震盪指標的K線，用於判斷市場的超買或超賣狀態。當K線在20以下並上穿D線時，通常被視為買入信號；當K線在80以上並下穿D線時，通常被視為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("D (Stochastic Oscillator)"), width=12),
                dbc.Col(html.P("用途：隨機震盪指標的D線，與K線結合使用，用於判斷市場的超買或超賣狀態。D線通常是K線的三日簡單移動平均。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("Stochastic RSI"), width=12),
                dbc.Col(html.P("用途：隨機指標和相對強弱指標的結合，用於識別超買和超賣狀態。Stochastic RSI 的值範圍從0到100，通常在20以下表示超賣，80以上表示超買。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("CCI (Commodity Channel Index)"), width=12),
                dbc.Col(html.P("用途：CCI 用於識別價格的超買和超賣狀態。當CCI值高於100時，表示市場超買；當CCI值低於-100時，表示市場超賣。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("Williams %R"), width=12),
                dbc.Col(html.P("用途：Williams %R 用於識別市場的超買和超賣狀態。其值範圍從-100到0，當值在-80以下時，表示市場超賣；在-20以上時，表示市場超買。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("ADX (Average Directional Index)"), width=12),
                dbc.Col(html.P("用途：ADX 用於測量趨勢的強度，而不是趨勢的方向。當ADX值高於25時，表示強趨勢；當ADX值低於20時，表示趨勢較弱或市場無趨勢。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("Close Price"), width=12),
                dbc.Col(html.P("用途：收盤價是當天交易結束時的最後價格，用於判斷當日的市場情況。收盤價是大多數技術分析指標的基礎。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ])
        ]
    elif button_id == "btn-combo-strategy":
        return 'btn-modern btn-modern-secondary', 'btn-modern btn-modern-primary', [
            dbc.Row([
                dbc.Col(html.H3("MACD 和 RSI 的組合策略"), width=12),
                dbc.Col(html.P("MACD 和 RSI 是兩個最常用的技術指標。當兩者結合使用時，可以提高交易信號的準確性。例如，當 RSI 低於 30 並且 MACD 線上穿信號線時，通常被視為強烈的買進信號；反之，當 RSI 高於 70 並且 MACD 線下穿信號線時，通常被視為強烈的賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("SMA 和 EMA 的組合策略"), width=12),
                dbc.Col(html.P("SMA 和 EMA 都是移動平均線指標，但 EMA 對價格變動更敏感。當短期 EMA 上穿長期 SMA 時，通常被視為買進信號；反之，當短期 EMA 下穿長期 SMA 時，通常被視為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("布林帶和 KDJ 的組合策略"), width=12),
                dbc.Col(html.P("布林帶用於判斷市場的波動性，而 KDJ 是基於隨機指標的技術指標。當價格接近布林帶下軌且 KDJ 中的 K 線上穿 D 線時，通常被視為買進信號；反之，當價格接近布林帶上軌且 K 線下穿 D 線時，通常被視為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("Stochastic RSI 和 CCI 的組合策略"), width=12),
                dbc.Col(html.P("Stochastic RSI 和 CCI 結合使用可以提高判斷超買和超賣狀態的準確性。當 Stochastic RSI 和 CCI 同時在超賣區域（如 Stochastic RSI < 20 且 CCI < -100），通常被視為買進信號；反之，當兩者同時在超買區域（如 Stochastic RSI > 80 且 CCI > 100），通常被視為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("斜率方向指標 (ADX) 和趨勢指標的組合策略"), width=12),
                dbc.Col(html.P("ADX 用於衡量趨勢的強度，而其他趨勢指標（如 EMA）可以用來判斷趨勢的方向。當 ADX 值高於 25，表示趨勢強勁，此時如果 EMA 顯示上升趨勢，則為買進信號；反之，當 ADX 值高於 25 且 EMA 顯示下降趨勢時，則為賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ]),
            dbc.Row([
                dbc.Col(html.H3("龍虎大賽策略"), width=12),
                dbc.Col(html.P("這是一種綜合策略，結合了多種指標，如 MACD、RSI、布林帶、KDJ 等。當多個指標同時發出買進信號（如 RSI 低於 30，MACD 上穿信號線，價格接近布林帶下軌且 K 線上穿 D 線），通常被視為強烈的買進信號；反之，當多個指標同時發出賣出信號，則為強烈的賣出信號。"), width=12),
                dbc.Col(html.Hr(), width=12)
            ])
        ]

if __name__ == '__main__':
    app.run_server(debug=True)