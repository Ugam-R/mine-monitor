import sqlite3
import pandas as pd
import numpy as np

DB_NAME = "mine_data.db"
OUTPUT_FILE = "processed_data.csv"


def load_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT
        timestamp,
        methane_raw,
        accel_x,
        accel_y,
        accel_z,
        force_raw,
        flex_raw,
        moisture_raw,
        roof_distance_cm
    FROM sensor_data
    ORDER BY timestamp
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def preprocess(df):
    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Replace invalid ultrasonic readings
    df["roof_distance_cm"] = df["roof_distance_cm"].replace(-1, np.nan)

    # Remove completely duplicated rows
    df = df.drop_duplicates()

    # Fill missing numeric values using nearby readings
    numeric_columns = [
        "methane_raw",
        "accel_x",
        "accel_y",
        "accel_z",
        "force_raw",
        "flex_raw",
        "moisture_raw",
        "roof_distance_cm"
    ]

    df[numeric_columns] = df[numeric_columns].interpolate(
        method="linear"
    )

    # Accelerometer magnitude
    df["accel_magnitude"] = np.sqrt(
        df["accel_x"] ** 2 +
        df["accel_y"] ** 2 +
        df["accel_z"] ** 2
    )

    # Sensor change from previous reading
    df["methane_delta"] = df["methane_raw"].diff()
    df["force_delta"] = df["force_raw"].diff()
    df["flex_delta"] = df["flex_raw"].diff()
    df["moisture_delta"] = df["moisture_raw"].diff()
    df["distance_delta"] = df["roof_distance_cm"].diff()

    # Rolling averages to reduce short-term noise
    df["methane_avg"] = df["methane_raw"].rolling(5).mean()
    df["force_avg"] = df["force_raw"].rolling(5).mean()
    df["flex_avg"] = df["flex_raw"].rolling(5).mean()
    df["moisture_avg"] = df["moisture_raw"].rolling(5).mean()
    df["distance_avg"] = df["roof_distance_cm"].rolling(5).mean()

    # First few rows have no previous/rolling values
    df = df.dropna().reset_index(drop=True)

    return df


def main():
    print("Loading sensor data...")
    df = load_data()

    print(f"Raw rows: {len(df)}")

    df = preprocess(df)

    print(f"Processed rows: {len(df)}")

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved processed dataset to: {OUTPUT_FILE}")
    print()
    print("Columns:")
    print(list(df.columns))


if __name__ == "__main__":
    main()
