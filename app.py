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
# LOAD MODEL SAFELY
# -----------------------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = pickle.load(open(model_path, "rb"))

# -----------------------------
# HTML FORM
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

    <!-- INSTRUCTIONS SECTION -->
    <div style="margin-bottom:15px; font-size:13px; color:#555;">
        <b>Instructions:</b><br>
        Enter customer details to predict churn risk.<br>
        Example ranges:<br>
        Tenure: 1–72 months<br>
        Monthly Charges: 20–120<br>
        Total Charges: 20–8000
    </div>

    <!--  EXAMPLE CUSTOMER -->
    <div style="font-size:12px; margin-bottom:15px; color:#777;">
        <b>Example high-risk customer:</b><br>
        Tenure: 2<br>
        Monthly Charges: 95<br>
        Total Charges: 190<br>
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

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return html_form

# -----------------------------
# PREDICT ROUTE (SAFE)
# -----------------------------
@app.route('/predict', methods=['POST'])
def predict():

    try:
        tenure = int(request.form['tenure'])
        monthly_charges = float(request.form['monthly_charges'])
        total_charges = float(request.form['total_charges'])
    except:
        return "Invalid input"

    contract_type = request.form['contract_type']
    internet_service = request.form['internet_service']

    # -----------------------------
    # ENCODING (must match training)
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

    input_data = [
        tenure,
        monthly_charges,
        total_charges,
        contract_map.get(contract_type, 0),
        internet_map.get(internet_service, 0)
    ]

    model_input = pd.DataFrame([input_data])

    # -----------------------------
    # PREDICTION
    # -----------------------------
    prediction = model.predict(model_input)[0]

    # -----------------------------
    # RESULT
    # -----------------------------
    if prediction == 1:
        result = "Customer is likely to CHURN"
    else:
        result = "Customer is NOT likely to churn"

    # -----------------------------
    # RETURN PAGE
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
                width: 500px;
                text-align: center;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
            }}

            h1 {{
                color: #1e3c72;
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

            <a href="/" class="button">Try Again</a>

        </div>
    </body>
    </html>
    """

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)