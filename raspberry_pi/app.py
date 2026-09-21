from flask import Flask, render_template, jsonify
import sqlite3
import math

app = Flask(__name__)

DB_NAME = "mine_data.db"


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

    if row:
        return dict(row)

    return None


def calculate_risk(data):
    score = 0

    # Force / load
    force = data["force_raw"]

    if force > 800:
        score += 30
    elif force > 500:
        score += 20
    elif force > 250:
        score += 10

    # Flex / deformation
    flex = data["flex_raw"]

    if flex < 500 or flex > 850:
        score += 25
    elif flex < 580 or flex > 800:
        score += 15

    # Moisture
    moisture = data["moisture_raw"]

    if moisture < 700:
        score += 20
    elif moisture < 850:
        score += 10

    # Accelerometer
    x = data["accel_x"]
    y = data["accel_y"]
    z = data["accel_z"]

    magnitude = math.sqrt(
        x * x +
        y * y +
        z * z
    )

    if magnitude > 800:
        score += 20
    elif magnitude > 650:
        score += 10

    # Roof distance
    distance = data["roof_distance_cm"]

    if distance >= 0:
        if distance < 50:
            score += 25

    score = min(score, 100)

    if score >= 75:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/latest")
def latest_data():
    data = get_latest_data()

    if data is None:
        return jsonify({
            "status": "no_data"
        })

    score, level = calculate_risk(data)

    data["risk_score"] = score
    data["risk_level"] = level

    return jsonify(data)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )