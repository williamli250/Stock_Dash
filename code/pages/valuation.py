from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行

    dbc.Row([
        dbc.Col(html.A(html.Button("回首頁", className="btn btn-primary", style={'float': 'right'}), href="/"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.H1("Stock Valuation", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行

    # 其他的預測頁面內容...
], fluid=True)