# GitHub Copilot: create a script that trains a classifier from training_data.csv
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from app.services.classifier import train_classifier, save_model


def load_csv(path="training_data.csv"):
    texts = []
    labels = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                texts.append(r.get("text", ""))
                labels.append(r.get("category", ""))
    except FileNotFoundError:
        print("training_data.csv not found. Create a CSV with columns 'text' and 'category'.")
    return texts, labels


def main():
    texts, labels = load_csv()
    if not texts:
        return
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    vec, model = train_classifier(X_train, y_train)
    preds = model.predict(vec.transform(X_test))
    print("Accuracy:", accuracy_score(y_test, preds))
    save_model(vec, model)


if __name__ == "__main__":
    main()
