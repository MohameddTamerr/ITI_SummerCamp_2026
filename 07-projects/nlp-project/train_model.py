import os
import re
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import joblib
import nbformat as nbf

def main():
    print("Loading dataset...")
    df = pd.read_csv("AI_Human.csv")
    print(f"Dataset shape: {df.shape}")
    
    # Handle any nulls if present
    df = df.dropna().reset_index(drop=True)
    df["generated"] = df["generated"].astype(int)
    
    # Subsample if needed for efficient training while preserving high accuracy
    # Using 100,000 samples for high training quality and rapid inference
    sample_size = min(100000, len(df))
    df_sampled, _ = train_test_split(df, train_size=sample_size, stratify=df["generated"], random_state=42)
    print(f"Sampled shape for training: {df_sampled.shape}")
    
    X = df_sampled["text"]
    y = df_sampled["generated"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=50000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english"
        )),
        ("classifier", LogisticRegression(
            C=5.0,
            max_iter=1000,
            random_state=42
        ))
    ])
    
    print("Training pipeline...")
    pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Human-written", "AI-generated"]))
    
    # Save the pipeline
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "ai_text_classifier.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
    
    # Test predictions
    sample_human = "Cars have been around since they became famous in the 1900s. People drive them every day to commute to work and go to school."
    sample_ai = "The socio-economic implications of automated transport infrastructure delineate a paradigm shift in urban logistics, optimizing resource allocation across macro-scale distribution networks."
    
    print(f"Sample Human Prediction: {pipeline.predict([sample_human])[0]}, Prob: {pipeline.predict_proba([sample_human])[0]}")
    print(f"Sample AI Prediction: {pipeline.predict([sample_ai])[0]}, Prob: {pipeline.predict_proba([sample_ai])[0]}")

if __name__ == "__main__":
    main()
