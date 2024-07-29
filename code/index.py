from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
from pages.dashboard import layout as dashboard_layout
from pages.valuation import layout as valuation_layout
from pages.indicator_intro import layout as indicator_intro_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Loading(
        id="loading",
        type="dot",
        fullscreen=True,
        className='dash-loading'
    )
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return html.Div([
            dcc.Loading(id="loading-dashboard", children=[
                html.Div(id="dashboard-content")
            ])
        ])
    elif pathname == '/valuation':
        return valuation_layout
    elif pathname == '/indicator-intro':
        return indicator_intro_layout
    else:
        return dbc.Container([
            dbc.Row([dbc.Col(html.Br()) for _ in range(2)]),  # 添加換行

            dbc.Row([
                dbc.Col(html.H1("William's DSS", className="text-center text-primary mb-4"), width=12)
            ]),
            dbc.Row([
                dbc.Col(
                    html.A(
                        html.Div("數位儀表板", className="square", style={
                            'width': '300px',
                            'height': '300px',
                            'background-color': 'rgba(173, 216, 230, 0.5)',  # 半透明的淺藍色
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'font-size': '40px',
                            'color': 'black',
                            'textDecoration': 'none'  # 移除文字下的底線
                        }),
                        href="/dashboard",
                        style={'textDecoration': 'none'}  # 移除文字下的底線
                    ), width=4, className="d-flex justify-content-center"
                ),
                dbc.Col(
                    html.A(
                        html.Div("指標介紹", className="square", style={
                            'width': '300px',
                            'height': '300px',
                            'background-color': 'rgba(255, 182, 193, 0.5)',  # 半透明的粉色
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'font-size': '40px',
                            'color': 'black',
                            'textDecoration': 'none'  # 移除文字下的底線
                        }),
                        href="/indicator-intro",
                        style={'textDecoration': 'none'}  # 移除文字下的底線
                    ), width=4, className="d-flex justify-content-center"
                ),
                dbc.Col(
                    html.A(
                        html.Div("估價", className="square", style={
                            'width': '300px',
                            'height': '300px',
                            'background-color': 'rgba(255, 255, 0, 0.5)',  # 半透明的黃色
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'font-size': '40px',
                            'color': 'black',
                            'textDecoration': 'none'  # 移除文字下的底線
                        }),
                        href="/valuation",
                        style={'textDecoration': 'none'}  # 移除文字下的底線
                    ), width=4, className="d-flex justify-content-center"
                )
            ], style={'margin': '100px'})  # 調整間距
        ], fluid=True)

@app.callback(
    Output('dashboard-content', 'children'),
    Input('url', 'pathname')
)
def load_dashboard_content(pathname):
    if pathname == '/dashboard':
        return dashboard_layout
    return html.Div()

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)