from flask import Flask, request, render_template_string
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Simple HTML form (no templates needed yet)
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

@app.route('/')
def home():
    return html_form

@app.route('/predict', methods=['POST'])
def predict():

    # -----------------------------
    # Get form data
    # -----------------------------
    tenure = float(request.form['tenure'])
    monthly = float(request.form['monthly_charges'])
    total = float(request.form['total_charges'])
    contract = request.form['contract_type']
    internet = request.form['internet_service']

    # -----------------------------
    # Create dataframe
    # -----------------------------
    input_data = pd.DataFrame([{
        "tenure": tenure,
        "monthly_charges": monthly,
        "total_charges": total,
        "contract_type": contract,
        "internet_service": internet
    }])

    # -----------------------------
    # One-hot encoding
    # -----------------------------
    input_data = pd.get_dummies(input_data)

    # -----------------------------
    # Match training columns
    # -----------------------------
    model_input = pd.DataFrame(0, columns=model.feature_names_in_, index=[0])
    model_input.update(input_data)

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = model.predict(model_input)[0]

    # -----------------------------
    # Business logic / suggestions
    # -----------------------------
    suggestions = []

    if tenure < 12:
        suggestions.append("Customers with very low tenure are more likely to churn.")

    if monthly > 80:
        suggestions.append("High monthly charges may increase churn risk.")

    if contract == "Month-to-month":
        suggestions.append("Month-to-month contracts often show higher churn rates.")

    if internet == "Fiber optic":
        suggestions.append("Fiber optic customers in telecom datasets often display higher churn behaviour.")

    if prediction == 1:
        result = "Customer is likely to CHURN"

        recommendation = """
        Recommended Actions:
        <ul>
            <li>Offer loyalty discounts or bundled plans</li>
            <li>Promote long-term contracts</li>
            <li>Provide proactive customer support outreach</li>
            <li>Review pricing sensitivity</li>
        </ul>
        """

    else:
        result = "Customer is NOT likely to churn"

        recommendation = """
        Retention Strengths:
        <ul>
            <li>Longer tenure improves customer stability</li>
            <li>Balanced pricing reduces churn probability</li>
            <li>Long-term contracts improve retention</li>
            <li>Customer profile appears relatively stable</li>
        </ul>

        <br>

        <b>Potential Risk Factors That Could Increase Churn:</b>
        <ul>
            <li>Increasing monthly charges significantly</li>
            <li>Reducing contract commitment</li>
            <li>Poor customer support experience</li>
            <li>Lower engagement over time</li>
        </ul>
        """

    # -----------------------------
    # Convert suggestions into HTML
    # -----------------------------
    suggestion_html = "<ul>"

    for item in suggestions:
        suggestion_html += f"<li>{item}</li>"

    suggestion_html += "</ul>"

    # -----------------------------
    # Styled result page
    # -----------------------------
    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Prediction Result</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            .container {{
                background: white;
                width: 650px;
                padding: 40px;
                border-radius: 12px;
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

            <h3>Model Interpretation</h3>

            {suggestion_html}

            <h3>Business Recommendations</h3>

            {recommendation}

            <a href="/" class="button">Try Another Prediction</a>

        </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)