import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# -----------------------
# STEP 1: Load dataset
# -----------------------
data = pd.read_csv("data/churn.csv")

print("Dataset preview:")
print(data.head())

# -----------------------
# STEP 2: Convert text columns into numbers
# -----------------------
data = pd.get_dummies(data, drop_first=True)

# -----------------------
# STEP 3: Split features and target
# -----------------------
X = data.drop("churn", axis=1)
y = data["churn"]

# -----------------------
# STEP 4: Train-test split
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------
# STEP 5: Train model
# -----------------------
model = LogisticRegression()
model.fit(X_train, y_train)

# -----------------------
# STEP 6: Check accuracy
# -----------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# -----------------------
# STEP 7: Save model
# -----------------------
pickle.dump(model, open("model.pkl", "wb"))

print("Model saved successfully!")