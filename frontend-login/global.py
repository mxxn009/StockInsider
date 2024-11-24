import flask
from flask import send_file
from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import time


# Initialize Flask app and configure extensions
app1 = flask.Flask(__name__)
app1.secret_key = 'your_secret_key'  # Set a secret key for sessions

bcrypt = Bcrypt(app1)

# In-memory user data (replace SQLAlchemy database with a dictionary)
users = {}

# Initialize Dash app
dash_app = dash.Dash(__name__, server=app1, url_base_pathname='/dashboard/')

# Sample data for Dash plot
np.random.seed(42)
df = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", periods=100),
    "Value": np.random.randn(100).cumsum()  # Cumulative sum of random values
})

# Define Dash layout with interactive elements
dash_app.layout = html.Div([
    html.H1("Sample Dashboard", style={'textAlign': 'center', 'color': '#2C8C99'}),

    # Dropdown for selecting the type of chart
    html.Div([
        html.Label("Select Chart Type:"),
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Scatter Plot', 'value': 'scatter'}
            ],
            value='line',  # default value
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),

    # Graph to display the chart
    dcc.Graph(id='main-graph'),

    # Slider for selecting the range of data to plot
    html.Div([
        html.Label("Select Range of Data:"),
        dcc.Slider(
            id='date-slider',
            min=0,
            max=len(df) - 1,
            step=1,
            value=99,  # default value
            marks={i: df['Date'][i].strftime('%Y-%m-%d') for i in range(0, len(df), 10)},
            tooltip={'placement': 'bottom', 'always_visible': True}
        )
    ], style={'width': '80%', 'margin': '0 auto', 'padding': '20px 0'}),

    html.Div([
        html.P("Adjust the slider and select different chart types to explore the data."),
        html.P("This is a simple dashboard built with Dash and Plotly.")
    ], style={'textAlign': 'center', 'color': '#888'})
])

# Callback to update the graph based on selected chart type and slider value
@dash_app.callback(
    dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('chart-type', 'value'),
     dash.dependencies.Input('date-slider', 'value')]
)
def update_graph(chart_type, date_range):
    # Slice the dataframe based on the selected range
    filtered_df = df.iloc[:date_range+1]

    # Create the figure based on the chart type selected
    if chart_type == 'line':
        trace = go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Value'],
            mode='lines',
            name='Value Over Time'
        )
    elif chart_type == 'bar':
        trace = go.Bar(
            x=filtered_df['Date'],
            y=filtered_df['Value'],
            name='Value Over Time'
        )
    elif chart_type == 'scatter':
        trace = go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df['Value'],
            mode='markers',
            name='Value Over Time'
        )

    layout = go.Layout(
        title='Sample Data Visualization',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Value'},
        hovermode='closest'
    )

    return {'data': [trace], 'layout': layout}

# Route for home page
@app1.route('/', methods=['GET', 'POST'])
def home():
    return render_template('intro.html')

@app1.route('/login', methods=['GET', 'POST'])
def login():
    time.sleep(0.5)
    return render_template('login.html')

# Route for login/signup page
@app1.route('/login_signup', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        action = request.form.get('action')  # 'login' or 'signup'
        
        if action == 'login':
            email = request.form['email']
            password = request.form['password']

            # Check if user exists and if password is correct
            user = users.get(email)
            if user and bcrypt.check_password_hash(user['password'], password):
                session['user_id'] = email  # Store user email in session
                session['username'] = user['name']  # Store username in session
                flash("Login successful!", 'success')
                return redirect(url_for('dashboard'))  # Redirect to the dashboard page

            else:
                flash("Login failed. Check your email and/or password.", 'danger')

        elif action == 'signup':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            # Check if user already exists
            if email in users:
                flash("Email already exists!", 'danger')
            else:
                # Store user in the in-memory dictionary
                users[email] = {'name': name, 'email': email, 'password': hashed_password}
                flash("Account created successfully!", 'success')
                return redirect(url_for('login_signup'))  # Stay on the same page

    return render_template('login.html')

# Route for dashboard page (only accessible after login)

@app1.route('/dashboard')
def homepage():
    # return render_template('home.html')
    return redirect('http://127.0.0.1:8050/')
def dashboard():
    if 'user_id' not in session:
        flash("You need to log in first.", 'warning')
        return redirect(url_for('login'))
    
    return redirect(url_for('homepage'))  # Return the Dash app directly when logged in

# Route for logging out
@app1.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", 'info')
    return redirect(url_for('login_signup'))

if __name__ == '__main__':
    app1.run(debug=True)
