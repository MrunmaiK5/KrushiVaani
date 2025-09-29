import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_crop_recommendation_model():
    """
    Train a RandomForestClassifier for crop recommendation
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, "data", "crop_recommendation.csv")

    print(f"Loading crop recommendation dataset from: {data_path}")
    df = pd.read_csv(data_path)
    
    print(f"Dataset loaded successfully. Shape: {df.shape}")
    print(f"Features: {df.columns.tolist()}")
    print(f"Target classes: {df['label'].unique()}")
    print(f"Number of samples per class:\n{df['label'].value_counts()}")
    
    # Define features and target
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target = 'label'
    
    X = df[features]
    y = df[target]
    
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Target vector shape: {y.shape}")
    
    # Split the data into train and test sets
    print("\nSplitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train RandomForestClassifier
    print("\nTraining RandomForestClassifier...")
    rf_classifier = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    rf_classifier.fit(X_train, y_train)
    
    # Make predictions
    print("Making predictions...")
    y_pred = rf_classifier.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Evaluation:")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Print detailed classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': rf_classifier.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Save the trained model
    print("\nSaving trained model...")
    model_path = 'crop_model.pkl'
    joblib.dump(rf_classifier, model_path)
    print(f"Model saved successfully as: {model_path}")
    
    # Also save feature names for later use
    feature_names_path = 'feature_names.pkl'
    joblib.dump(features, feature_names_path)
    print(f"Feature names saved as: {feature_names_path}")
    
    return rf_classifier, accuracy

if __name__ == "__main__":
    try:
        model, accuracy = train_crop_recommendation_model()
        print(f"\nTraining completed successfully!")
        print(f"Final model accuracy: {accuracy:.4f}")
    except Exception as e:
        print(f"Error during training: {str(e)}")
        raise
