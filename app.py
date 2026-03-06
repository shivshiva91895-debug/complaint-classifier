from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

HISTORY_FILE = "history.csv"


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


def read_history():
    history = []
    try:
        with open(HISTORY_FILE, newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                history.append(row)
    except:
        pass
    return history


def save_history(complaint, category):
    from datetime import datetime

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("history.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([complaint, category, time])

@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None

    if request.method == "POST":
        complaint = request.form["complaint"]

        prediction = predict_category(complaint)

        save_history(complaint, prediction)

    history = read_history()

    stats = {
        "Delivery Issue": 0,
        "Refund Issue": 0,
        "Payment Issue": 0,
        "Product Issue": 0
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


@app.route("/clear")
def clear():

    with open(HISTORY_FILE, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Complaint", "Category", "Time"])

    return index()


if __name__ == "__main__":
    app.run(debug=True)