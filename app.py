import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, session, jsonify
import yfinance as yf
import os
from functools import wraps
import requests
import time
import datetime

app = Flask(__name__)
from extra_stuff import show_close_plot, show_combine_plot, show_high_plot, show_low_plot
app.secret_key = 'your_secret_key'
from flask_restx import Api, Resource, fields

def get_symbol_from_name(company_name):
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]  # most relevant match
    else:
        return None

global_data = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return render_template('login.html', error=None)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    """
    This function renders the home page of the application.

    Returns:
        render_template: The rendered HTML template for the home page.
    """
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Hardcoded credentials for demo
        if username == 'admin' and password == 'password123':
            session['authenticated'] = True
            return render_template('index.html')
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

api = Api(app, version="1.0", title="Stock Analysis API", description="A simple Stock Analysis API", doc="/docs")

index_np = api.namespace("Index", description="Index operations", path="/index")
analysis_np = api.namespace("Analysis", description="Analysis operations", path="/analysis")
home_np = api.namespace("Home", description="Home operations", path="/home")
login_np = api.namespace("Login", description="Login operations", path="/login")

input_model = api.model("InputModel", {
    "stockname": fields.String(required=True, description="Stock name"),
    "startDate": fields.String(required=True, description="Start date in YYYY-MM-DD format"),
    "endDate": fields.String(required=True, description="End date in YYYY-MM-DD format")
})

# @login_np.route("/")
# @login_required
# def home():
#     """
#     This function renders the home page of the application.
# 
#     Returns:
#         render_template: The rendered HTML template for the home page.
#     """
#     return render_template("index.html")



@index_np.route("/")
class IndexResource(Resource):
  def get(self):
    """
    API Home Endpoint

    Returns a message informing users that the home page is a sign-up page and they must fill in the required entries.
    """
    return {
      "message": "Welcome to TrendWise! Please visit the home page (/) and fill in all required fields to sign up."
    }



@analysis_np.route("/")
class AnalysisResource(Resource):
  @analysis_np.expect(input_model)
  def post(self):
    """
     Perform stock analysis based on user input.
     This endpoint allows users to input a stock name and a date range,
     and it returns an analysis of the stock's performance during that period.
    **Request Body:**
      - `stockname`: (str) The stock name to analyze.
      - `startDate`: (str) The start date for the analysis in YYYY-MM-DD format.
      - `endDate`: (str) The end date for the analysis in YYYY-MM-DD format.
    **Returns**:
        `str`: Rendered HTML template with stock analysis results.
    """
    stockname = api.payload.get("stockname")
    startDate = api.payload.get("startDate")
    endDate = api.payload.get("endDate")
    df = yf.download(stockname, start= f"{startDate}", end= f"{endDate}")
    high = round(df["High"].max()[0], 2)
    low = round(df["Low"].min()[0], 2)
    show_close_plot(df)
    show_combine_plot(df)
    show_high_plot(df)
    show_low_plot(df)
    ticker = yf.Ticker(stockname)
    info = ticker.get_info()
    og_name = info.get("longName")
    
    
    sector = info.get("sector")
    industry = info.get("industry")
    ceo = info.get("companyOfficers", [{}])[0].get("name")
    headquarters = f"{info.get('city')}, {info.get('country')}" if info.get("city") and info.get("country") else None

    market_cap = info.get("marketCap")
    pe_ratio_forward = info.get("forwardPE")
    pe_ratio_trailing = info.get("trailingPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")

    return render_template("analysis.html", stockname=stockname, startDate=startDate, endDate=endDate, high=high, low=low, og_name=og_name, sector=sector, industry=industry, ceo=ceo, headquarters=headquarters, market_cap=market_cap, pe_ratio_forward=pe_ratio_forward, pe_ratio_trailing=pe_ratio_trailing, eps=eps, dividend_yield=dividend_yield, fifty_two_week_high=fifty_two_week_high, fifty_two_week_low=fifty_two_week_low)


@home_np.route("/", methods=["POST"])
class HomeResource(Resource):
    def post(self):
        """API Home Endpoint.
        **Returns**
        a message indicating that the API is running and ready for use."""        
        return {"message": "Welcome to the Stock Analysis API!"}

@app.route("/home", methods=["POST"])
def signup():
  username = request.form.get("Username")
  session["username"] = username
  return render_template("home.html", username = username)  
nnew = "hello"
@app.route("/intro")
def intro():
  return render_template("intro.html", nnew= nnew)

@app.route("/hello")
def hello():
    return "Hello, World!"


@app.route("/mistake")
def mistake():
  return "<h1>Kindly Sign-up First</h1>"

@app.route("/analysis", methods=["POST"])
def mainpage():
    stockname = request.form.get("stockname")
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")

    df = yf.download(stockname, start=startDate, end=endDate)

    high = round(df["High"].max().iloc[0], 2)
    low = round(df["Low"].min().iloc[0], 2)

    # Generate plots and get filenames
    close_img = show_close_plot(df, stockname, startDate, endDate)
    high_img = show_high_plot(df, stockname, startDate, endDate)
    low_img = show_low_plot(df, stockname, startDate, endDate)
    combined_img = show_combine_plot(df, stockname, startDate, endDate)

    ticker = yf.Ticker(stockname)
    info = ticker.get_info()
    og_name = info.get("longName")

    sector = info.get("sector")
    industry = info.get("industry")
    ceo = info.get("companyOfficers", [{}])[0].get("name")
    headquarters = f"{info.get('city')}, {info.get('country')}" if info.get("city") and info.get("country") else None

    market_cap = info.get("marketCap")
    pe_ratio_forward = info.get("forwardPE")
    pe_ratio_trailing = info.get("trailingPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")

    return render_template("analysis.html",
        stockname=stockname,
        startDate=startDate,
        endDate=endDate,
        high=high,
        low=low,
        og_name=og_name,
        sector=sector,
        industry=industry,
        ceo=ceo,
        headquarters=headquarters,
        market_cap=market_cap,
        pe_ratio_forward=pe_ratio_forward,
        pe_ratio_trailing=pe_ratio_trailing,
        eps=eps,
        dividend_yield=dividend_yield,
        fifty_two_week_high=fifty_two_week_high,
        fifty_two_week_low=fifty_two_week_low,
        close_img=close_img,
        high_img=high_img,
        low_img=low_img,
        combined_img=combined_img
    )

@app.route('/delete-images', methods=['POST'])
def delete_images():
    data = request.get_json()
    images = data.get('images', [])
    deleted = []
    for img in images:
        if img:
            img_path = os.path.join(app.root_path, 'static', img)
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                    deleted.append(img)
                except Exception as e:
                    pass  # Optionally log error
    return jsonify({'deleted': deleted})

















# @app.route("/about", methods=["POST"])
# def sign_up():
#   if not email or not password:
#         return "Missing email or password", 400 
#   return f"Your email is: {email}\n Your Password is: {password}"


# email = request.form.get("Email")
# password = request.form.get("Password")







if __name__ == "__main__":
  app.run(debug= True)
