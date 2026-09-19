import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression

import pickle


# Read dataset

data = pd.read_csv(
    "../dataset/resumes.csv"
)


# Convert text into numbers

vectorizer = TfidfVectorizer()


X = vectorizer.fit_transform(
    data["resume_text"]
)


y = data["label"]


# Create AI model

model = LogisticRegression()


# Train model

model.fit(
    X,
    y
)


# Save trained model

pickle.dump(
    model,
    open("../model.pkl","wb")
)


# Save text converter

pickle.dump(
    vectorizer,
    open("../vectorizer.pkl","wb")
)


print("Model Training Completed")