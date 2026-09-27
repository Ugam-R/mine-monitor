import os
import sqlite3
import joblib
import pandas as pd
import numpy as np


DB_NAME = "mine_data.db"
MODEL_FILE = "ml/models/random_forest.joblib"


def get_latest_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def create_features(data):
    """
    Create the feature vector required by the trained model.

    Rolling and baseline values are estimated from
    the latest available database readings.
    """

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query("""
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 10
    """, conn)

    conn.close()

    if df.empty:
        return None

    df = df.iloc[::-1].reset_index(drop=True)

    # Replace invalid ultrasonic readings
    df.loc[
        (df["roof_distance_cm"] < 20) |
        (df["roof_distance_cm"] > 300),
        "roof_distance_cm"
    ] = np.nan

    df["roof_distance_cm"] = (
        df["roof_distance_cm"].interpolate()
    )

    # Acceleration magnitude
    df["accel_magnitude"] = np.sqrt(
        df["accel_x"] ** 2 +
        df["accel_y"] ** 2 +
        df["accel_z"] ** 2
    )

    sensor_columns = [
        "methane_raw",
        "force_raw",
        "flex_raw",
        "moisture_raw",
        "roof_distance_cm",
        "accel_magnitude"
    ]

    # Baselines and deviations
    for column in sensor_columns:
        df[f"{column}_baseline"] = (
            df[column]
            .rolling(
                window=10,
                min_periods=1
            )
            .median()
        )

        df[f"{column}_deviation"] = (
            df[column] -
            df[f"{column}_baseline"]
        )

    # Delta features
    df["methane_delta"] = df["methane_raw"].diff()
    df["force_delta"] = df["force_raw"].diff()
    df["flex_delta"] = df["flex_raw"].diff()
    df["moisture_delta"] = df["moisture_raw"].diff()
    df["distance_delta"] = df["roof_distance_cm"].diff()

    # Rolling averages
    df["methane_avg"] = (
        df["methane_raw"].rolling(5).mean()
    )

    df["force_avg"] = (
        df["force_raw"].rolling(5).mean()
    )

    df["flex_avg"] = (
        df["flex_raw"].rolling(5).mean()
    )

    df["moisture_avg"] = (
        df["moisture_raw"].rolling(5).mean()
    )

    df["distance_avg"] = (
        df["roof_distance_cm"].rolling(5).mean()
    )

    # Change features
    df["force_change"] = df["force_raw"].diff()
    df["flex_change"] = df["flex_raw"].diff()
    df["moisture_change"] = df["moisture_raw"].diff()
    df["distance_change"] = df["roof_distance_cm"].diff()
    df["methane_change"] = df["methane_raw"].diff()

    # Trend features
    df["force_trend"] = (
        df["force_raw"].rolling(5).mean().diff()
    )

    df["flex_trend"] = (
        df["flex_raw"].rolling(5).mean().diff()
    )

    df["moisture_trend"] = (
        df["moisture_raw"].rolling(5).mean().diff()
    )

    df["distance_trend"] = (
        df["roof_distance_cm"].rolling(5).mean().diff()
    )

    df["methane_trend"] = (
        df["methane_raw"].rolling(5).mean().diff()
    )

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.ffill().bfill()

    return df.iloc[-1]


def predict():
    if not os.path.exists(MODEL_FILE):
        print("Model not found.")
        return

    package = joblib.load(MODEL_FILE)

    model = package["model"]
    feature_columns = package["feature_columns"]
    training_ranges = package["training_ranges"]

    latest = get_latest_data()

    if latest is None:
        print("No sensor data available.")
        return

    features = create_features(latest)

    if features is None:
        print("Unable to create features.")
        return

    X = pd.DataFrame(
        [
            [
                features[column]
                for column in feature_columns
            ]
        ],
        columns=feature_columns
    )

    prediction = model.predict(X)[0]

    # Check whether live values are outside
    # the range seen during model training.
    out_of_range = []

    for column in feature_columns:
        value = float(X.iloc[0][column])

        minimum = training_ranges[column]["min"]
        maximum = training_ranges[column]["max"]

        if value < minimum or value > maximum:
            out_of_range.append({
                "feature": column,
                "value": round(value, 2),
                "training_min": round(minimum, 2),
                "training_max": round(maximum, 2)
            })

    print("====================================")
    print(" ML Risk Prediction")
    print("====================================")

    print(
        "Training range status:",
        "OUT OF RANGE"
        if out_of_range
        else "WITHIN RANGE"
    )

    if out_of_range:
        print("\nOut-of-range features:")

        for item in out_of_range:
            print(
                f"{item['feature']}: "
                f"{item['value']} "
                f"(training range "
                f"{item['training_min']} - "
                f"{item['training_max']})"
            )

    print("\nPrediction:", prediction)

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(X)[0]

        print("\nConfidence:")

        for label, probability in zip(
            model.classes_,
            probabilities
        ):
            print(
                f"{label}: "
                f"{probability * 100:.2f}%"
            )


if __name__ == "__main__":
    predict()
