## This file carries out the prediction once article titles are fed into the ML model.

import os
import joblib
from data.preprocessing import clean_text as cleantext

ML_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and vectorizer from ml/
model_path = os.path.join(ML_DIR, "article_classifier.joblib")
vectorizer_path = os.path.join(ML_DIR, "vectorizer.joblib")

clf = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def predict_title(text):
    process_text = cleantext(text)
    X = vectorizer.transform([process_text])
    prediction = clf.predict(X)[0]
    # Get probability/confidence for the predicted class
    proba = clf.predict_proba(X)[0]
    # Find the index of the predicted class
    class_index = list(clf.classes_).index(prediction)
    confidence = proba[class_index]
    return prediction, confidence

def prediction(article_titles):
    lst = []
    for entry in article_titles:
        prediction_label, confidence = predict_title(entry)
        if prediction_label == "interested":
            lst.append((entry, confidence))

    if not lst:
        return "No interesting articles found today. 😞"
    
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst[0][0]