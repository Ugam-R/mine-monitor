import serial
import json
import sqlite3
from datetime import datetime

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600
DB_NAME = "mine_data.db"

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    methane_raw INTEGER,
    accel_x INTEGER,
    accel_y INTEGER,
    accel_z INTEGER,
    force_raw INTEGER,
    flex_raw INTEGER,
    moisture_raw INTEGER,
    roof_distance_cm REAL
)
""")

conn.commit()

print("====================================")
print(" Mine Monitoring Data Logger")
print("====================================")
print("Arduino connected.")
print("Logging sensor data...")
print()

while True:
    try:
        line = arduino.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        data = json.loads(line)

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        cursor.execute("""
        INSERT INTO sensor_data (
            timestamp,
            methane_raw,
            accel_x,
            accel_y,
            accel_z,
            force_raw,
            flex_raw,
            moisture_raw,
            roof_distance_cm
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            data["methane_raw"],
            data["accel_x"],
            data["accel_y"],
            data["accel_z"],
            data["force_raw"],
            data["flex_raw"],
            data["moisture_raw"],
            data["roof_distance_cm"]
        ))

        conn.commit()

        print(
            timestamp,
            "| MQ4:", data["methane_raw"],
            "| ACC:",
            data["accel_x"],
            data["accel_y"],
            data["accel_z"],
            "| FSR:", data["force_raw"],
            "| FLEX:", data["flex_raw"],
            "| MOIST:", data["moisture_raw"],
            "| DIST:", data["roof_distance_cm"]
        )

    except json.JSONDecodeError:
        print("Invalid JSON received, skipping...")

    except KeyboardInterrupt:
        print("\nLogger stopped.")
        break

conn.close()
arduino.close()