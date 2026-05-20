# -----------------------------
# IMPORTS
# -----------------------------
from flask import Flask, request
import pickle
import pandas as pd
import os

# -----------------------------
# APP INIT
# -----------------------------
app = Flask(__name__)

# -----------------------------
# LOAD MODEL
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = pickle.load(open(model_path, "rb"))

# -----------------------------
# HOME PAGE (HTML FORM)
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
            width: 420px;
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
    </style>
</head>

<body>

<div class="container">

    <h2>Customer Churn Prediction</h2>

    <!-- Instructions -->
    <div style="font-size:13px; color:#555; margin-bottom:10px;">
        <b>Instructions:</b><br>
        Tenure: 1–72 months<br>
        Monthly Charges: 20–120<br>
        Total Charges: 20–8000
    </div>

    <!-- Example -->
    <div style="font-size:12px; color:#777; margin-bottom:10px;">
        <b>Example High Risk:</b><br>
        Tenure: 2<br>
        Monthly: 95<br>
        Total: 190<br>
        Contract: Month-to-month<br>
        Internet: Fiber optic
    </div>

    <form method="POST" action="/predict">

        <label>Tenure</label>
        <input name="tenure" type="number" value="12" required>

        <label>Monthly Charges</label>
        <input name="monthly_charges" type="number" value="70" required>

        <label>Total Charges</label>
        <input name="total_charges" type="number" value="1000" required>

        <label>Contract Type</label>
        <select name="contract_type">
            <option>Month-to-month</option>
            <option>One year</option>
            <option>Two year</option>
        </select>

        <label>Internet Service</label>
        <select name="internet_service">
            <option>DSL</option>
            <option>Fiber optic</option>
            <option>No</option>
        </select>

        <input type="submit" value="Predict Churn">
    </form>

</div>

</body>
</html>
"""

# -----------------------------
# ROUTES
# -----------------------------
@app.route('/')
def home():
    return html_form


@app.route('/predict', methods=['POST'])
def predict():

    # -----------------------------
    # INPUTS
    # -----------------------------
    try:
        tenure = int(request.form['tenure'])
        monthly_charges = float(request.form['monthly_charges'])
        total_charges = float(request.form['total_charges'])
    except:
        return "Invalid input"

    contract_type = request.form['contract_type']
    internet_service = request.form['internet_service']

    # -----------------------------
    # CREATE DATAFRAME
    # -----------------------------
    input_df = pd.DataFrame([{
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract_type": contract_type,
        "internet_service": internet_service
    }])

    # -----------------------------
    # ONE HOT ENCODING
    # -----------------------------
    model_input = pd.get_dummies(input_df)

    # -----------------------------
    # ALIGN FEATURES (CRITICAL FIX)
    # -----------------------------
    model_input = model_input.reindex(columns=model.feature_names_in_, fill_value=0)

    # -----------------------------
    # PREDICTION
    # -----------------------------
    prediction = model.predict(model_input)[0]

    # -----------------------------
    # BUSINESS INSIGHTS (ADDED BACK)
    # -----------------------------
    suggestions = []

    if tenure < 12:
        suggestions.append("Low tenure increases churn risk.")

    if monthly_charges > 80:
        suggestions.append("High monthly charges increase churn risk.")

    if contract_type == "Month-to-month":
        suggestions.append("Month-to-month contracts increase churn risk.")

    if internet_service == "Fiber optic":
        suggestions.append("Fiber optic customers often show higher churn.")

    suggestion_html = "<ul>" + "".join(f"<li>{s}</li>" for s in suggestions) + "</ul>"

    # -----------------------------
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

    # -----------------------------
    # RESULT PAGE
    # -----------------------------
    return f"""
    <html>
    <head>
        <title>Result</title>
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
                width: 550px;
                text-align: center;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
            }}

            h1 {{
                color: #1e3c72;
            }}

            h3 {{
                color: #2a5298;
            }}

            li {{
                font-size: 16px;
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

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)