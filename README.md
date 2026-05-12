# Customer Churn Prediction & Visualisation

## Introduction

Customer retention has become one of the most important challenges faced by subscription-based industries such as telecommunications, banking, streaming platforms, and digital services. Businesses often spend significantly more money acquiring new customers than retaining existing ones. As a result, understanding why customers leave and predicting potential churn behaviour has become a major application area for data analytics and machine learning.

This project was developed as an end-to-end machine learning and analytics application focused on predicting telecom customer churn behaviour using customer subscription and billing-related information. Rather than approaching the project solely as a modelling exercise, the system was designed to simulate how predictive analytics solutions are implemented in real business environments.

The project combines multiple stages of the data science workflow including:
- data preprocessing
- feature engineering
- machine learning model development
- backend integration using Flask
- user interface design
- prediction interpretation
- business recommendation generation

The final application allows users to input customer-related attributes and receive:
- real-time churn predictions
- business-oriented interpretation
- actionable customer retention recommendations

The objective was not only to build a machine learning model, but also to understand how analytics systems are designed, integrated, and presented as usable products.

---

# Project Objectives

The primary aim of this project was to understand how machine learning models can support customer retention strategies and business decision-making processes.

The project specifically focused on:

- analysing customer behaviour associated with churn
- building a machine learning classification model
- integrating the trained model into a Flask web application
- designing a user-friendly prediction interface
- generating interpretable business recommendations
- understanding deployment-oriented machine learning workflows
- applying version control practices using Git and GitHub

In addition to predictive modelling, the project also served as a practical introduction to backend development, debugging workflows, and full-stack machine learning integration.

---

# Business Context

Customer churn is a major operational and financial challenge in telecom companies. Losing existing customers impacts long-term profitability and customer acquisition costs are often substantially higher than retention costs.

Predictive analytics systems can help organisations identify high-risk customers before they leave, allowing companies to take proactive retention measures such as:
- loyalty incentives
- pricing adjustments
- customer support intervention
- personalised service offerings
- long-term subscription plans

This project attempts to simulate a simplified version of such a customer analytics solution using machine learning techniques and interactive web technologies.

---

# Dataset Description

The project uses a telecom-style customer churn dataset containing customer subscription details, billing information, and service-related attributes. The dataset was structured to simulate real-world customer retention analytics scenarios commonly seen in telecom and subscription-based industries.

The dataset includes both numerical and categorical variables, allowing the project to demonstrate practical preprocessing and feature engineering techniques required for machine learning workflows.

## Key Variables Included

| Feature | Description |
|---|---|
| tenure | Number of months the customer remained with the service |
| monthly_charges | Monthly billing amount charged to the customer |
| total_charges | Total cumulative charges incurred by the customer |
| contract_type | Type of customer subscription contract |
| internet_service | Type of internet service used |
| churn | Target variable indicating customer churn behaviour |

## Target Variable

The target variable used for prediction is:

- `1` → Customer churned
- `0` → Customer retained

The dataset was intentionally structured to support supervised machine learning classification workflows and customer behaviour analysis.

---

# Methodology

The project followed a structured machine learning workflow beginning from data preprocessing and continuing through model training, backend integration, and interactive prediction generation.

## Data Loading

The dataset was loaded using the pandas library from a CSV file stored within the project structure.

This stage introduced:
- dataset handling
- tabular data manipulation
- data ingestion workflows

---

## Data Preprocessing

Machine learning models cannot directly interpret categorical text-based variables. Therefore, preprocessing techniques were applied to transform customer subscription categories into numerical representations.

Categorical variables such as:
- contract type
- internet service category

were converted into machine-readable numerical features using one-hot encoding.

This step ensured compatibility between the dataset and the Logistic Regression model.

---

## Feature Engineering

The dataset was separated into:
- input features (`X`)
- target variable (`y`)

This allowed customer behaviour indicators to be isolated from the churn outcome variable.

Feature engineering is an important stage within machine learning because models learn patterns from engineered numerical representations rather than raw business data alone.

---

## Train-Test Split

To evaluate model generalisation performance, the dataset was divided into:
- training dataset
- testing dataset

using an 80-20 split ratio.

This ensures that the model is evaluated using previously unseen data rather than memorising training observations.

---

## Model Development

A Logistic Regression classification model was selected for the initial implementation because of:
- simplicity
- interpretability
- suitability for binary classification problems

The model was implemented using scikit-learn and trained on the processed customer dataset.

Although relatively simple, Logistic Regression remains widely used in industry for baseline predictive analytics systems and interpretable binary classification tasks.

---

## Model Evaluation

The trained model was evaluated using prediction accuracy on the testing dataset.

The project achieved successful churn classification performance while demonstrating the complete machine learning workflow including:
- preprocessing
- training
- inference
- deployment preparation

---

## Model Serialization

After training, the machine learning model was serialised into a `.pkl` file using Python’s `pickle` module.

This allowed the trained model to be reused inside the Flask application without retraining during every execution.

The serialised model acts as the deployable “brain” of the application.

---

# Flask Backend Integration

The project integrates the trained machine learning model into a Flask-based backend application.

The Flask backend is responsible for:
- routing web requests
- receiving user input
- preprocessing incoming data
- loading the trained model
- generating real-time predictions
- rendering prediction results dynamically

The application demonstrates how machine learning systems are operationalised into user-facing software products.

---

# User Interface Design

The web interface was developed using HTML and CSS integrated directly within the Flask application.

The interface was intentionally designed to provide:
- a modern gradient-based visual design
- structured form layout
- user-friendly prediction workflow
- styled prediction result cards
- business-oriented recommendation sections

The objective was to move beyond a simple command-line machine learning script and instead simulate a lightweight analytics application experience.

---

# Prediction Interpretation & Recommendation System

Rather than returning only raw model outputs, the application includes a lightweight business interpretation layer designed to simulate decision-support analytics systems.

The system analyses risk-related behavioural indicators such as:
- low customer tenure
- high monthly charges
- month-to-month subscription structures
- internet service patterns

Based on these indicators, the application generates business-oriented recommendations related to:
- customer retention
- pricing sensitivity
- loyalty improvement
- contract optimisation

This additional interpretation layer improves explainability and demonstrates how machine learning outputs can support business decision-making processes.

---

# Results & Insights

The final application successfully demonstrates a complete end-to-end machine learning workflow integrated into a web-based analytics system.

The system is capable of:
- accepting customer-related inputs
- preprocessing user data
- generating churn predictions
- interpreting behavioural risk indicators
- providing retention-focused recommendations

Several behavioural trends associated with churn risk were identified throughout implementation, particularly:
- shorter customer tenure
- higher monthly billing charges
- flexible month-to-month contracts

The project additionally demonstrated how predictive analytics can be translated into interpretable business insights rather than remaining as isolated statistical outputs.

---

# Technologies Used

## Programming Language
- Python

## Machine Learning Libraries
- scikit-learn
- pandas

## Backend Framework
- Flask

## Frontend Technologies
- HTML
- CSS

## Version Control
- Git
- GitHub

## Development Environment
- Visual Studio Code

---

# Project Structure

```plaintext
churn-web-app/
│
├── app.py
├── model.py
├── model.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── churn.csv
│
├── venv/
