import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yfinance as yf
import plotly.graph_objs as go
import datetime as dt
import time


# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "StockInsider"


# Inline styles
styles = {
    'body': {
        'margin': '0',
        'padding': '0',
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f0f7f8',
        'minHeight': '100vh',
    },
    'dashboard': {
        'display': 'flex',
        'maxWidth': '1400px',
        'margin': '20px auto',
        'backgroundColor': 'white',
        'borderRadius': '20px',
        'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.05)',
        'overflow': 'hidden',
    },
    'sidebar': {
        'width': '240px',
        'backgroundColor': 'white',
        'padding': '24px',
        'borderRight': '1px solid #f0f0f0',
    },
    'logo': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '8px',
        'color': '#00a5a5',
        'fontWeight': '600',
        'marginBottom': '32px',
    },
    'navItem': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '12px',
        'padding': '12px',
        'color': '#666',
        'textDecoration': 'none',
        'borderRadius': '8px',
        'marginBottom': '4px',
    },
    'navItemActive': {
        'backgroundColor': '#e6f7f7',
        'color': '#00a5a5',
    },
    'mainContent': {
        'flex': '1',
        'padding': '32px',
        'backgroundColor': '#fff',
    },
    'header': {
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'marginBottom': '32px',
    },
    'welcome': {
        'fontSize': '24px',
        'fontWeight': '600',
        'color': '#333',
    },
    'metrics': {
        'display': 'flex',
        'gap': '24px',
        'marginBottom': '32px',
    },
    'metricCard': {
        'backgroundColor': 'white',
        'border': '1px solid #eee',
        'borderRadius': '12px',
        'padding': '20px',
        'flex': '1',
    },
    'metricLabel': {
        'color': '#666',
        'fontSize': '14px',
        'marginBottom': '8px',
    },
    'metricValue': {
        'fontSize': '24px',
        'fontWeight': '600',
        'color': '#333',
    },
    'chart': {
        'backgroundColor': 'white',
        'border': '1px solid #eee',
        'borderRadius': '12px',
        'padding': '20px',
        'marginBottom': '32px',
    },
    'table': {
        'backgroundColor': 'white',
        'border': '1px solid #eee',
        'borderRadius': '12px',
        'padding': '20px',
    },
    'tableHeader': {
        'display': 'grid',
        'gridTemplateColumns': 'auto 1fr repeat(4, auto)',
        'gap': '16px',
        'padding': '12px',
        'borderBottom': '1px solid #eee',
        'fontWeight': '500',
        'color': '#666',
    },
    'tableRow': {
        'display': 'grid',
        'gridTemplateColumns': 'auto 1fr repeat(4, auto)',
        'gap': '16px',
        'padding': '12px',
        'borderBottom': '1px solid #f5f5f5',
        'alignItems': 'center',
    },
    'rightPanel': {
        'width': '300px',
        'padding': '24px',
        'borderLeft': '1px solid #f0f0f0',
    },
    'profile': {
        'width': '40px',
        'height': '40px',
        'borderRadius': '50%',
        'backgroundColor': '#f0f0f0',
    },
    'topSites': {
        'marginTop': '32px',
    },
    'siteItem': {
        'display': 'flex',
        'justifyContent': 'space-between',
        'padding': '12px 0',
        'borderBottom': '1px solid #f5f5f5',
    },
    'searchBar': {
        'display': 'flex',
        'marginBottom': '20px',
    },
    'searchInput': {
        'flex': '1',
        'padding': '10px',
        'border': '1px solid #ddd',
        'borderRadius': '4px 0 0 4px',
        'fontSize': '16px',
    },
    'searchButton': {
        'padding': '10px 20px',
        'backgroundColor': '#00a5a5',
        'color': 'white',
        'border': 'none',
        'borderRadius': '0 4px 4px 0',
        'cursor': 'pointer',
        'fontSize': '16px',
    },
}

# App layout
app.layout = html.Div(style=styles['body'], children=[
    html.Div(style=styles['dashboard'], children=[
        html.Aside(style=styles['sidebar'], children=[
            html.Div(style=styles['logo'], children="StockInsider"),
            html.Nav(children=[
                html.A("Home", href="#", style={**styles['navItem'], **styles['navItemActive']}),
                html.Div([
                    html.A("Favourites", href="http://127.0.0.1:3000/favourites.html", style=styles['navItem']),
                    html.Div(id='page-content'),
                ]),
                # html.A("Favourites", href="#", style=styles['navItem']),
                dcc.Location(id="url", refresh=False),
                html.Div([
                    html.A("Community", href="http://127.0.0.1:3000/community.html", style=styles['navItem']),
                    html.Div(id='page-content'),
                ]),
                # html.A("Community", href="/community", style=styles['navItem']),
                html.A("Blog", href="#", style=styles['navItem']),
                html.A("Support", href="#", style=styles['navItem']),
                html.A("Settings", href="#", style=styles['navItem']),
            ]),
        ]),
        html.Main(style=styles['mainContent'], children=[
            html.Header(style=styles['header'], children=[
                html.H1("Welcome back", style=styles['welcome']),
            ]),
            html.Div(style=styles['metrics'], children=[
                html.Div(style=styles['metricCard'], children=[
                    html.Div("Revenue", style=styles['metricLabel']),
                    html.Div("₹1,392.28", style=styles['metricValue']),
                ]),
                html.Div(style=styles['metricCard'], children=[
                    html.Div("Invested", style=styles['metricLabel']),
                    html.Div("₹25,491.72", style=styles['metricValue']),
                ]),
            ]),
            html.Div(style=styles['searchBar'], children=[
                dcc.Input(id="stock-symbol", type="text", placeholder="Enter Stock Symbol (e.g., RELIANCE.NS)", style=styles['searchInput']),
                html.Button("Search", id="search-button", n_clicks=0, style=styles['searchButton']),
            ]),
            html.Div(id="stock-details", style=styles['metricCard']),
            html.Div(style=styles['chart'], children=[
                dcc.Graph(id="stock-graph"),
            ]),
            html.Div(style=styles['table'], children=[
                html.Div(style=styles['tableHeader'], children=[
                    html.Div("Platform"),
                    html.Div("Date"),
                    html.Div("Status"),
                    html.Div("Amount"),
                    html.Div("Commission"),
                ]),
                html.Div(style=styles['tableRow'], children=[
                    html.Div("Groww"),
                    html.Div("2023-11-24"),
                    html.Div("Active"),
                    html.Div("₹386.40"),
                    html.Div("₹11.64"),
                ]),
                html.Div(style=styles['tableRow'], children=[
                    html.Div("Zerodha"),
                    html.Div("2023-11-24"),
                    html.Div("Active"),
                    html.Div("₹292.80"),
                    html.Div("₹32.92"),
                ]),
            ]),
        ]),
        html.Aside(style=styles['rightPanel'], children=[
            html.Div(style=styles['profile']),
            html.Div(style=styles['topSites'], children=[
                html.H3("My Top Sites"),
                html.Div(style=styles['siteItem'], children=[
                    html.Span("Groww"),
                    html.Span("₹432.8"),
                ]),
                html.Div(style=styles['siteItem'], children=[
                    html.Span("Zerodha"),
                    html.Span("₹399.1"),
                ]),
                html.Div(style=styles['siteItem'], children=[
                    html.Span("Upstox"),
                    html.Span("₹346.8"),
                ]),
            ]),
        ]),
    ]),
    dcc.Interval(id="update-interval", interval=60000, n_intervals=0),
])

# Keep the existing callback functions unchanged
# @app.callback(
#     [Output("page-content", "children")],
#     [Input("url", "pathname")],
# )
@app.callback(
    [Output("stock-details", "children"), Output("stock-graph", "figure")],
    [Input("search-button", "n_clicks"), Input("update-interval", "n_intervals")],
    [State("stock-symbol", "value")],
)
def update_dashboard(n_clicks, n_intervals, stock_symbol):
    if not stock_symbol:
        stock_symbol = "^NSEI"  # Nifty 50 symbol

    try:
        stock_data = fetch_stock_data(stock_symbol)

        if stock_data.empty:
            return html.P("No data available for this symbol."), go.Figure()

        current_price = stock_data["Close"].iloc[-1]
        open_price = stock_data["Open"].iloc[0]
        change = round(current_price - open_price, 2)
        percent_change = round((change / open_price) * 100, 2)

        stock_info = [
            html.H3(f"{yf.Ticker(stock_symbol).info.get('longName', 'Nifty 50')} ({stock_symbol.upper()})", style={'fontSize': '1.5rem', 'marginBottom': '1rem'}),
            html.P(f"Current Price: ₹{current_price:.2f}", style={'marginBottom': '0.5rem'}),
            html.P(f"Change: ₹{change} ({percent_change}%)", style={'marginBottom': '0.5rem', 'color': 'green' if change > 0 else 'red'}),
        ]
        
        market_cap = yf.Ticker(stock_symbol).info.get('marketCap')
        if market_cap:
            stock_info.append(html.P(f"Market Cap: ₹{market_cap:,}", style={'marginBottom': '0.5rem'}))

        fifty_two_week_low = yf.Ticker(stock_symbol).info.get("fiftyTwoWeekLow")
        fifty_two_week_high = yf.Ticker(stock_symbol).info.get("fiftyTwoWeekHigh")
        if fifty_two_week_low and fifty_two_week_high:
            stock_info.append(html.P(f"52 Week Range: ₹{fifty_two_week_low} - ₹{fifty_two_week_high}", style={'marginBottom': '0.5rem'}))

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=stock_data.index,
                y=stock_data["Close"],
                mode="lines",
                line=dict(color="#00a5a5"),
                name="Close Price",
            )
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            title="6-Month Stock Price Trend",
            font=dict(size=15),
            height=400,
        )

        return stock_info, fig

    except Exception as e:
        return [html.P(f"Error: {str(e)}", style={'color': 'red'})], go.Figure()

# Keep the helper functions unchanged
def is_market_closed():
    now_utc = dt.datetime.utcnow()
    now_ist = now_utc + dt.timedelta(hours=5, minutes=30)
    today = now_ist.date()

    market_open = dt.time(9, 0)
    market_close = dt.time(16, 0)
    weekday = now_ist.weekday()  # Monday = 0, Sunday = 6

    if weekday >= 5 or not (market_open <= now_ist.time() <= market_close):
        return True
    return False

def fetch_stock_data(stock_symbol):
    now_utc = dt.datetime.utcnow()
    now_ist = now_utc + dt.timedelta(hours=5, minutes=30)
    today = now_ist.date()
    six_months_ago = today - dt.timedelta(days=180)

    ticker = yf.Ticker(stock_symbol)
    stock_data = ticker.history(start=six_months_ago, end=today, interval="1d")

    return stock_data

if __name__ == "__main__":
    time.sleep(1)
    app.run_server(debug=True)