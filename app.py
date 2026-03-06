from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

history_file = "history.csv"


# Complaint classification
def predict_category(text):

    text = text.lower()

    if "delay" in text or "late" in text:
        return "Delivery Issue"

    elif "refund" in text:
        return "Refund Issue"

    elif "payment" in text:
        return "Payment Issue"

    elif "product" in text or "damage" in text:
        return "Product Issue"

    else:
        return "Other Issue"


# Read complaint history
def read_history():

    history = []

    try:
        with open(history_file, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                history.append(row)

    except:
        pass

    return history


# Save complaint
def save_history(complaint, category):

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_file, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([complaint, category, time])


# Main page
@app.route("/", methods=["GET","POST"])
def index():

    prediction = None

    if request.method == "POST":

       complaint = request.form["complaint"]

if complaint.strip() != "":
    prediction = predict_category(complaint)
    save_history(complaint, prediction)
else:
    prediction = None

    history = read_history()

    stats = {
        "Delivery Issue":0,
        "Refund Issue":0,
        "Payment Issue":0,
        "Product Issue":0
    }

    for row in history:

        cat = row["Category"]

        if cat in stats:
            stats[cat] += 1

    return render_template(
        "index.html",
        prediction=prediction,
        history=history,
        total=len(history),
        stats=stats
    )


# Clear history
@app.route("/clear")
def clear():

    with open(history_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(["Complaint","Category","Time"])

    return index()


import os

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)