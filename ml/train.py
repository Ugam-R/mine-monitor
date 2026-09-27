import os
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import joblib


FEATURE_FILE = "ml/data/features.csv"
MODEL_FILE = "ml/models/random_forest.joblib"


def create_labels(df):
    """
    Create prototype risk labels using heuristic sensor conditions.

    IMPORTANT:
    These labels are for demonstrating the ML pipeline only.
    They are NOT validated mine-safety labels.
    """

    score = np.zeros(len(df))

    score += np.where(
        df["force_raw"] > 800,
        30,
        0
    )

    score += np.where(
        (df["force_raw"] > 500) &
        (df["force_raw"] <= 800),
        20,
        0
    )

    score += np.where(
        (df["force_raw"] > 250) &
        (df["force_raw"] <= 500),
        10,
        0
    )

    flex_deviation = abs(df["flex_raw"] - 675)

    score += np.where(
        flex_deviation > 200,
        25,
        0
    )

    score += np.where(
        (flex_deviation > 100) &
        (flex_deviation <= 200),
        15,
        0
    )

    score += np.where(
        (flex_deviation > 50) &
        (flex_deviation <= 100),
        5,
        0
    )

    score += np.where(
        df["moisture_raw"] < 700,
        20,
        0
    )

    score += np.where(
        (df["moisture_raw"] >= 700) &
        (df["moisture_raw"] < 850),
        10,
        0
    )

    acceleration_change = abs(
        df["accel_magnitude"] - 620
    )

    score += np.where(
        acceleration_change > 80,
        20,
        0
    )

    score += np.where(
        (acceleration_change > 40) &
        (acceleration_change <= 80),
        10,
        0
    )

    score += np.where(
        df["roof_distance_cm"] < 50,
        25,
        0
    )

    score += np.where(
        (df["roof_distance_cm"] >= 50) &
        (df["roof_distance_cm"] < 100),
        10,
        0
    )

    score = np.clip(score, 0, 100)

    labels = np.where(
        score >= 75,
        "CRITICAL",
        np.where(
            score >= 50,
            "HIGH",
            np.where(
                score >= 25,
                "MEDIUM",
                "LOW"
            )
        )
    )

    return labels


def main():
    print("Loading feature dataset...")

    df = pd.read_csv(FEATURE_FILE)

    print(f"Rows: {len(df)}")

    df["risk_level"] = create_labels(df)

    print("\nPrototype label distribution:")
    print(df["risk_level"].value_counts())

    feature_columns = [
        "methane_raw",
        "accel_x",
        "accel_y",
        "accel_z",
        "force_raw",
        "flex_raw",
        "moisture_raw",
        "roof_distance_cm",
        "accel_magnitude",
        "methane_delta",
        "force_delta",
        "flex_delta",
        "moisture_delta",
        "distance_delta",
        "methane_avg",
        "force_avg",
        "flex_avg",
        "moisture_avg",
        "distance_avg",
        "methane_raw_deviation",
        "force_raw_deviation",
        "flex_raw_deviation",
        "moisture_raw_deviation",
        "roof_distance_cm_deviation",
        "accel_magnitude_deviation",
        "force_change",
        "flex_change",
        "moisture_change",
        "distance_change",
        "methane_change",
        "force_trend",
        "flex_trend",
        "moisture_trend",
        "distance_trend",
        "methane_trend"
    ]

    X = df[feature_columns]
    y = df["risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print(f"\nTraining rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    print("\nTraining Random Forest...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nModel evaluation")
    print("================")
    print(f"Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    os.makedirs(
        "ml/models",
        exist_ok=True
    )

    # Save the training ranges so the live prediction
    # system can detect out-of-distribution values.
    training_ranges = {
        column: {
            "min": float(X[column].min()),
            "max": float(X[column].max())
        }
        for column in feature_columns
    }

    joblib.dump(
        {
            "model": model,
            "feature_columns": feature_columns,
            "training_ranges": training_ranges
        },
        MODEL_FILE
    )

    print(
        f"\nModel saved to: {MODEL_FILE}"
    )


if __name__ == "__main__":
    main()
