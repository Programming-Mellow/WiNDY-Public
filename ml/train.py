## This file trains the ML model for classification via interesting or not interesting with article titles.

import os
import pandas as pd
from data.preprocessing import clean_text as cleantext
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

ML_DIR = os.path.dirname(os.path.abspath(__file__))

# Load and clean data from ml/articles.csv
csv_path = os.path.join(ML_DIR, 'articles.csv')
df = pd.read_csv(csv_path, encoding='latin1')
texts = df['title'].tolist()
labels = df['label'].tolist()

cleaned_texts = [cleantext(text) for text in texts]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    cleaned_texts, labels, test_size=0.2, random_state=42
)

# Vectorize text
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# Evaluate
y_pred = clf.predict(X_test_vec)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and vectorizer in ml/
model_path = os.path.join(ML_DIR, "article_classifier.joblib")
vectorizer_path = os.path.join(ML_DIR, "vectorizer.joblib")
joblib.dump(clf, model_path)
joblib.dump(vectorizer, vectorizer_path)
print("Model and vectorizer saved in ml/ folder.")