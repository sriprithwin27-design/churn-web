# IMPORTS
# -----------------------------
from flask import Flask, request
import pickle
import pandas as pd
import os

# APP INITIALIZATION
# -----------------------------
app = Flask(__name__)

# LOAD MODEL SAFELY
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = pickle.load(open(model_path, "rb"))

# HTML FORM PAGE
# -----------------------------
html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Churn Prediction App</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            width: 400px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
        }

        h2 {
            text-align: center;
            color: #1e3c72;
        }

        input, select {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 6px;
            border: 1px solid #ccc;
        }

        input[type="submit"] {
            background: #1e3c72;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }

        input[type="submit"]:hover {
            background: #2a5298;
        }

        label {
            font-size: 14px;
            color: #333;
        }
    </style>
</head>

<body>

<div class="container">

    <h2>Customer Churn Prediction</h2>

    <form method="POST" action="/predict">

        <label>Tenure</label>
        <input name="tenure" type="number" required>

        <label>Monthly Charges</label>
        <input name="monthly_charges" type="number" required>

        <label>Total Charges</label>
        <input name="total_charges" type="number" required>

        <label>Contract Type</label>
        <select name="contract_type">
            <option value="Month-to-month">Month-to-month</option>
            <option value="One year">One year</option>
            <option value="Two year">Two year</option>
        </select>

        <label>Internet Service</label>
        <select name="internet_service">
            <option value="DSL">DSL</option>
            <option value="Fiber optic">Fiber optic</option>
            <option value="No">No</option>
        </select>

        <input type="submit" value="Predict Churn">
    </form>

</div>

</body>
</html>
"""

# HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return html_form

# PREDICTION ROUTE
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():

    # INPUT HANDLING
    # -----------------------------
    try:
        tenure = int(request.form['tenure'])
        monthly_charges = float(request.form['monthly_charges'])
        total_charges = float(request.form['total_charges'])
    except:
        return "Invalid input"

    contract_type = request.form['contract_type']
    internet_service = request.form['internet_service']

    # ENCODING
    # -----------------------------
    contract_map = {
        "Month-to-month": 0,
        "One year": 1,
        "Two year": 2
    }

    internet_map = {
        "DSL": 0,
        "Fiber optic": 1,
        "No": 2
    }

    contract_encoded = contract_map.get(contract_type, 0)
    internet_encoded = internet_map.get(internet_service, 0)

    # MODEL INPUT
    # -----------------------------
    input_data = [
        tenure,
        monthly_charges,
        total_charges,
        contract_encoded,
        internet_encoded
    ]

    model_input = pd.DataFrame([input_data])

    # PREDICTION
    # -----------------------------
    prediction = model.predict(model_input)[0]

    # INSIGHTS
    # -----------------------------
    suggestions = []

    if tenure < 12:
        suggestions.append("Low tenure increases churn risk.")

    if monthly_charges > 80:
        suggestions.append("High monthly charges increase churn risk.")

    if contract_type == "Month-to-month":
        suggestions.append("Month-to-month contracts have higher churn risk.")

    if internet_service == "Fiber optic":
        suggestions.append("Fiber optic customers often show higher churn.")

    suggestion_html = "<ul>" + "".join(f"<li>{s}</li>" for s in suggestions) + "</ul>"

    # RESULT LOGIC
    # -----------------------------
    if prediction == 1:
        result = "Customer is likely to CHURN"

        recommendation = """
        <ul>
            <li>Offer discounts or loyalty rewards</li>
            <li>Promote long-term contracts</li>
            <li>Improve customer engagement</li>
        </ul>
        """
    else:
        result = "Customer is NOT likely to churn"

        recommendation = """
        <ul>
            <li>Customer is stable</li>
            <li>Maintain service quality</li>
            <li>Monitor pricing changes</li>
        </ul>
        """

    # RESULT PAGE HTML
    # -----------------------------
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prediction Result</title>

        <style>
            body {{
                font-family: Arial;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}

            .container {{
                background: white;
                padding: 40px;
                border-radius: 12px;
                width: 650px;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
            }}

            h1 {{
                color: #1e3c72;
                text-align: center;
            }}

            h3 {{
                color: #2a5298;
            }}

            p, li {{
                font-size: 16px;
                line-height: 1.6;
                color: #333;
            }}

            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 12px 20px;
                background: #1e3c72;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
            }}

            .button:hover {{
                background: #2a5298;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>{result}</h1>

            <h3>Insights</h3>
            {suggestion_html}

            <h3>Recommendations</h3>
            {recommendation}

            <a href="/" class="button">Try Again</a>

        </div>

    </body>
    </html>
    """

# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)