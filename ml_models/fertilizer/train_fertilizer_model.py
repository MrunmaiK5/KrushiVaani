# ml-models/fertilizer/train_fertilizer_model.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def find_dataset():
    """Try several likely locations for fertilizer.csv and return first existing path."""
    base = os.path.dirname(os.path.abspath(__file__))  # ml-models/fertilizer
    candidates = [
        os.path.join(base, "fertilizer.csv"),
        os.path.join(base, "data", "fertilizer.csv"),
        os.path.join(base, "..", "fertilizer.csv"),
        os.path.join(os.getcwd(), "ml-models", "fertilizer", "fertilizer.csv"),
        os.path.join(os.getcwd(), "ml_models", "fertilizer", "fertilizer.csv"),
        os.path.join(os.getcwd(), "data", "fertilizer.csv"),
        "/mnt/data/fertilizer.csv",  # for interactive environments
    ]
    for p in candidates:
        if os.path.exists(p):
            return os.path.abspath(p)
    return None

def train_and_save():
    data_path = find_dataset()
    if data_path is None:
        raise FileNotFoundError(
            "Couldn't find fertilizer.csv. Checked common locations. "
            "Place your CSV in ml-models/fertilizer/fertilizer.csv or data/fertilizer.csv."
        )

    print("Loading dataset from:", data_path)
    df = pd.read_csv(data_path)
    # drop index column if present
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    required_cols = {"Crop", "N", "P", "K", "pH", "soil_moisture"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dataset missing required columns. Found columns: {df.columns.tolist()}")

    features = ["N", "P", "K", "pH", "soil_moisture"]
    target = "Crop"

    X = df[features]
    y = df[target]

    # Try to stratify when possible
    strat = y if (y.value_counts().min() >= 2) else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=strat
    )

    clf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model & feature names
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out_dir, exist_ok=True)
    model_path = os.path.join(out_dir, "fertilizer_model.pkl")
    features_path = os.path.join(out_dir, "feature_names.pkl")
    joblib.dump(clf, model_path)
    joblib.dump(features, features_path)
    print(f"\nSaved model to: {model_path}")
    print(f"Saved features to: {features_path}")

    return model_path, features_path

if __name__ == "__main__":
    try:
        train_and_save()
        print("Training finished.")
    except Exception as e:
        print("Error during training:", e)
        raise
