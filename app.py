from flask import Flask, render_template, request
import pandas as pd
import csv
import os
from datetime import datetime
import model

app = Flask(__name__)

history_file = "history.csv"

# Home page
@app.route("/")
def index():
    history = []
    if os.path.exists(history_file):
        df = pd.read_csv(history_file)
        history = df.to_dict(orient="records")
    return render_template("index.html", history=history)


# Predict complaint category
@app.route("/predict", methods=["POST"])
def predict():
    complaint = request.form["complaint"]

    category = model.predict_category(complaint)

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([complaint, category, time_now])

    return render_template("index.html", complaint=complaint, category=category)


# Clear history
@app.route("/clear")
def clear():
    with open(history_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Complaint", "Category", "Time"])

    return index()


# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)