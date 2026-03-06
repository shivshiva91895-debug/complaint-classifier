import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
data = pd.read_csv("complaints.csv")

X = data["Complaint"]
y = data["Category"]

vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vector, y)

def predict_category(text):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    return prediction[0]