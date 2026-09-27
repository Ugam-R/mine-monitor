import pandas as pd
import numpy as np
import os

INPUT_FILE = "ml/processed_data.csv"
OUTPUT_FILE = "ml/data/features.csv"


def create_features(df):
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Acceleration magnitude
    df["accel_magnitude"] = np.sqrt(
        df["accel_x"] ** 2 +
        df["accel_y"] ** 2 +
        df["accel_z"] ** 2
    )

    # Baseline and deviation features
    for column in [
        "methane_raw",
        "force_raw",
        "flex_raw",
        "moisture_raw",
        "roof_distance_cm",
        "accel_magnitude"
    ]:
        df[f"{column}_baseline"] = (
            df[column]
            .rolling(window=10, min_periods=1)
            .median()
        )

        df[f"{column}_deviation"] = (
            df[column] -
            df[f"{column}_baseline"]
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

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.dropna().reset_index(drop=True)

    return df


def main():
    print("Loading processed dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Input rows: {len(df)}")

    df = create_features(df)

    print(f"Feature rows: {len(df)}")
    print(f"Feature count: {len(df.columns)}")

    os.makedirs("ml/data", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved features to: {OUTPUT_FILE}")

    print()
    print("Features:")
    print(list(df.columns))


if __name__ == "__main__":
    main()
