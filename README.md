# StockInsider: An Integrated Flask and Dash Application

StockInsider is a web-based platform that combines Flask and Dash to deliver a seamless user experience for stock tracking, data visualization, and user management. The application supports user authentication, stock data visualization, and a responsive dashboard for interactive data exploration.

---

## Features

### Flask-Based Functionality
1. **User Authentication**: 
   - Login and signup functionality using Flask sessions.
   - Password hashing implemented with Flask-Bcrypt for secure storage.

2. **Session Management**:
   - Secure user sessions with Flask for storing user credentials.

3. **Routing**:
   - Multiple routes for login, signup, dashboard, and logout.
   - Clear separation between frontend pages and the integrated dashboard.

---

### Dash-Powered Visualization
1. **Interactive Dashboard**:
   - Built with Dash and Plotly for seamless data visualization.
   - Includes a line chart, bar chart, and scatter plot to display stock data.

2. **Data Filtering**:
   - Slider for filtering data based on date range.
   - Dropdown menu for selecting visualization types.

3. **Real-Time Updates**:
   - Dynamic data rendering based on user inputs.

---

### Sample Data
- Uses synthetic stock data generated with `numpy` and `pandas` for demonstration purposes.
- Dash supports real-time or historical data integration with minimal modification.

---

## Prerequisites

Before running the application, ensure the following dependencies are installed:

- Python 3.8+
- Required Python libraries:
  - `dash`
  - `flask`
  - `flask-bcrypt`
  - `plotly`
  - `numpy`
  - `pandas`
  - `yfinance` (optional for live stock data integration)

Install dependencies using the following command:

```bash
pip install -r requirements.txt
```

---

## Getting Started

### Running the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/StockInsider.git
   ```
2. Navigate to the project directory:
   ```bash
   cd StockInsider
   ```
3. Run the Flask app:
   ```bash
   python app1.py
   ```

### Access the Application
- Visit `http://127.0.0.1:5000` in your browser to access the Flask interface.
- The Dash dashboard is available at `http://127.0.0.1:8050` once logged in.

---

## Usage

1. **User Authentication**:
   - Register using the signup form.
   - Log in with the registered credentials.

2. **Interactive Dashboard**:
   - Use the dropdown to select the chart type.
   - Adjust the slider to filter data based on the date range.

3. **Logout**:
   - End the session by clicking the logout link.

---

## Customization

### Integrating Live Stock Data
- Replace the sample data in `app1.py` with data fetched from APIs like Yahoo Finance using the `yfinance` library.

### Styling
- Modify `static/styles.css` to customize the appearance of the web pages and dashboard.

---

## License
This project is open-source and available under the [MIT License](LICENSE). 

---

## Acknowledgments
- Flask: Simplified backend development.
- Dash: Powerful framework for building interactive data visualizations.
- Plotly: High-quality charting library. 
