# -*- coding: utf-8 -*-
"""code1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19_HO7Fd9GjroO95jnf8WObgM3polC1Jv
"""

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Function to clean text data
def clean_text(text):
    if not isinstance(text, str):
        return ""  # Handle non-string values
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\@w+|\#','', text)  # Remove @ and #
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuations
    return text

# Load datasets
training_data_path = '/content/twitter_training.csv'  # Replace with your file path
validation_data_path = '/content/twitter_validation.csv'  # Replace with your file path

training_data = pd.read_csv(training_data_path)
validation_data = pd.read_csv(validation_data_path)

# Apply text cleaning
training_data['cleaned_text'] = training_data.iloc[:, 3].apply(clean_text)
validation_data['cleaned_text'] = validation_data.iloc[:, 3].apply(clean_text)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
X_train = tfidf_vectorizer.fit_transform(training_data['cleaned_text'])
X_val = tfidf_vectorizer.transform(validation_data['cleaned_text'])

# Extracting target labels
y_train = training_data.iloc[:, 2]
y_val = validation_data.iloc[:, 2]

# Logistic Regression Model
model = LogisticRegression(max_iter=500)  # Adjust max_iter as needed
model.fit(X_train, y_train)

# Predictions and Evaluation
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
report = classification_report(y_val, y_pred)

# Output results
print("Accuracy:", accuracy)
print("Classification Report:\n", report)