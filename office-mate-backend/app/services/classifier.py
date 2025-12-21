from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_store", "classifier.joblib")


def train_classifier(train_texts, labels) -> Tuple[TfidfVectorizer, object]:
    vec = TfidfVectorizer(max_features=10000, stop_words="english")
    X = vec.fit_transform(train_texts)
    # choose a simple linear model
    model = LinearSVC()
    model.fit(X, labels)
    return vec, model


def save_model(vectorizer, model, path: str = MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({"vectorizer": vectorizer, "model": model}, path)


def load_model(path: str = MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError("model not found")
    obj = joblib.load(path)
    return obj["vectorizer"], obj["model"]


def predict_category(text: str) -> str:
    try:
        vec, model = load_model()
    except Exception:
        return "unknown"
    X = vec.transform([text])
    pred = model.predict(X)
    return str(pred[0])
