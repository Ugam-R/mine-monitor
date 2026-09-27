# Mine Monitor

## AI-Enabled Real-Time Mine Subsidence Monitoring & Early Warning System

**SIH26025 — Smart India Hackathon Project**

Mine Monitor is a low-cost prototype for monitoring structural and environmental conditions associated with underground coal-mine subsidence.

The system combines multiple sensors, an Arduino Nano, Raspberry Pi 4, SQLite, Flask, a real-time web dashboard, and a planned machine-learning pipeline.

> **Prototype Notice:** This repository contains an academic prototype. Sensor values, thresholds, and risk calculations require proper calibration, engineering validation, and real mine/field data before any operational deployment.

---

## Project Objective

The objective of Mine Monitor is to:

- Collect multiple sensor readings in real time
- Store and organize sensor data
- Monitor structural and environmental changes
- Combine multiple sensor parameters for risk assessment
- Provide a real-time monitoring dashboard
- Generate early warnings when abnormal conditions are detected
- Provide a foundation for machine-learning-based subsidence prediction

---

## System Architecture

The overall data flow is:

**Sensors → Arduino Nano → USB Serial → Raspberry Pi → SQLite → Flask API → Dashboard → Risk Engine / ML**

### System Components

| Component | Role |
|---|---|
| Sensors | Collect structural and environmental measurements |
| Arduino Nano | Reads sensor signals and sends JSON data |
| Raspberry Pi 4 | Processes data and hosts the backend |
| SQLite | Stores timestamped sensor readings |
| Flask | Provides the web application and API |
| Dashboard | Displays real-time monitoring information |
| Risk Engine | Calculates a prototype risk score |
| ML Pipeline | Performs future data-driven prediction |

---

## Hardware

| Component | Purpose |
|---|---|
| Raspberry Pi 4 Model B | Main processing unit and dashboard host |
| Arduino Nano | Sensor acquisition and serial communication |
| MQ-4 | Methane monitoring |
| ADXL335 | 3-axis motion, tilt and vibration monitoring |
| FSR | Force/load monitoring proxy |
| Flex Sensor | Deformation/bending monitoring |
| HC-SR04 | Roof-floor distance and convergence monitoring |
| Moisture Sensor | Ground moisture/seepage monitoring |
| Buzzer | Local warning indication |

---

## Sensor Parameters

### MQ-4 — Methane

The MQ-4 provides an analog sensor output that changes with methane concentration.

The current prototype stores the raw ADC reading.

**Important:** Raw ADC values should not be interpreted directly as methane concentration in ppm without proper calibration.

### ADXL335 — Accelerometer

The ADXL335 provides three analog axes:

- X
- Y
- Z

The readings can be used to monitor changes in movement, orientation, tilt, and vibration.

### FSR — Force Sensor

The Force Sensitive Resistor provides an analog response to applied force.

In the prototype it is treated as a force/load proxy.

Actual engineering units such as Newtons or kN require calibration and an appropriate mechanical installation.

### Flex Sensor

The flex sensor changes its resistance when bent.

It can be used as a prototype indicator of structural deformation or crack/fissure movement.

### HC-SR04 — Ultrasonic Sensor

The ultrasonic sensor measures the distance between the sensor and a surface.

In this prototype it is used to monitor roof-floor distance and potential roof convergence.

### Moisture Sensor

The moisture sensor measures changes in ground or soil moisture.

It can be used as an indicator of changing moisture or seepage conditions.

**It is not a direct pore-pressure measurement.**

---

## Arduino Sensor Node

The Arduino Nano reads the sensors and sends the measurements to the Raspberry Pi through USB serial communication.

The current serial configuration is:

- Baud rate: `9600`
- Serial device on Raspberry Pi: `/dev/ttyUSB0`
- Data format: JSON

Example packet:

```json
{
  "methane_raw": 130,
  "accel_x": 327,
  "accel_y": 392,
  "accel_z": 359,
  "force_raw": 10,
  "flex_raw": 675,
  "moisture_raw": 1011,
  "roof_distance_cm": 170.87
}
```

---

## Raspberry Pi Backend

The Raspberry Pi performs the main backend operations:

1. Receives sensor data through USB serial
2. Parses incoming JSON packets
3. Stores readings in SQLite
4. Provides data through a Flask API
5. Calculates a prototype risk score
6. Serves the monitoring dashboard

---

## Database

Sensor readings are stored locally using SQLite.

The main table is:

`sensor_data`

It contains:

- Timestamp
- Methane raw value
- Accelerometer X
- Accelerometer Y
- Accelerometer Z
- Force raw value
- Flex raw value
- Moisture raw value
- Roof distance

The local database file is excluded from Git using `.gitignore`.

---

## Monitoring Dashboard

The Flask dashboard provides a real-time view of the monitoring system.

The dashboard displays:

- Methane sensor readings
- Pillar load readings
- Deformation readings
- Ground moisture readings
- Roof convergence distance
- Accelerometer values
- Current risk score
- Current risk level
- System connection status
- Last update time

The dashboard communicates with the Flask API through:

`/api/latest`

---

## Prototype Risk Engine

The current backend contains a rule-based prototype risk engine.

The engine combines several sensor conditions into a risk score.

The prototype risk levels are:

- LOW
- MEDIUM
- HIGH
- CRITICAL

The current rules are intended only for prototype demonstration.

Future versions should incorporate:

- Sensor calibration
- Baseline estimation
- Noise filtering
- Sensor validation
- Rate-of-change analysis
- Moving averages
- Multi-sensor relationships
- Engineering thresholds
- Real mine datasets
- Machine-learning predictions

---

## Machine Learning Pipeline

The planned machine-learning pipeline is:

**Raw Sensor Data → Data Cleaning → Preprocessing → Feature Engineering → Model Training → Prediction → Early Warning**

Potential features include:

- Moving averages
- Sensor trends
- Rate of change
- Standard deviation
- Baseline deviation
- Accelerometer statistics
- Roof convergence rate
- Moisture variation
- Combined multi-sensor indicators
- Time-based features

A Random Forest model is planned as an initial baseline model.

More advanced sequential models can be evaluated if sufficient labelled time-series data becomes available.

---

## Dataset

A useful dataset for this project should contain timestamped sensor observations, engineered features, and appropriate labels or targets.

Example fields include:

| Field | Description |
|---|---|
| timestamp | Time of observation |
| methane_raw | MQ-4 raw reading |
| accel_x | Accelerometer X |
| accel_y | Accelerometer Y |
| accel_z | Accelerometer Z |
| force_raw | FSR raw reading |
| flex_raw | Flex sensor reading |
| moisture_raw | Moisture sensor reading |
| roof_distance_cm | Ultrasonic distance |
| engineered_features | Trends and statistical features |
| risk_label | Target/risk classification |

Prototype data can come from:

- Live sensor recordings
- Controlled experiments
- Simulated abnormal conditions
- Engineering or expert-defined prototype labels

Real mine or field data is required for meaningful validation of a subsidence prediction system.

---

## Project Structure

```text
mine-monitor/
|
├── README.md
├── requirements.txt
├── .gitignore
|
├── arduino/
|   └── mine_node/
|       └── mine_node.ino
|
├── raspberry_pi/
|   ├── app.py
|   ├── data_logger.py
|   ├── serial_test.py
|   |
|   ├── templates/
|   |   └── dashboard.html
|   |
|   └── static/
|       ├── css/
|       |   └── dashboard.css
|       |
|       └── js/
|           └── dashboard.js
|
├── ml/
|   ├── README.md
|   ├── preprocessing.py
|   ├── feature_engineering.py
|   ├── train.py
|   ├── predict.py
|   ├── data/
|   └── models/
|
├── docs/
|   ├── architecture/
|   ├── hardware/
|   ├── dataset/
|   └── presentation/
|
└── tests/
```

---

## Software Stack

- **C/C++** — Arduino firmware
- **Python** — Backend and data processing
- **Flask** — Web application and REST API
- **SQLite** — Local database
- **HTML** — Dashboard structure
- **CSS** — Dashboard styling
- **JavaScript** — Real-time dashboard updates
- **scikit-learn** — Planned machine-learning pipeline
- **Git/GitHub** — Version control and collaboration

---

## Running the Raspberry Pi Backend

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Connect the Arduino Nano to the Raspberry Pi through USB.

Check the serial device:

```bash
ls /dev/ttyUSB*
```

The current configuration expects:

```text
/dev/ttyUSB0
```

Start the data logger:

```bash
python3 data_logger.py
```

In another terminal, start the Flask application:

```bash
python3 app.py
```

The dashboard will be available at:

```text
http://<RASPBERRY_PI_IP>:5000
```

---

## Repository Safety

The following files are intentionally excluded from Git:

```text
*.db
*.sqlite
*.sqlite3
.env
__pycache__/
*.pyc
ml/models/*.pkl
ml/models/*.joblib
```

Local databases, environment files, and generated machine-learning models should not be committed unless intentionally versioned.

---

## Current Development Status

| Component | Status |
|---|---|
| Arduino sensor acquisition | Prototype |
| Serial communication | Prototype |
| SQLite data logging | Prototype |
| Flask backend | Prototype |
| Monitoring dashboard | Prototype |
| Rule-based risk engine | Prototype |
| Sensor calibration | Pending |
| Sensor filtering | Pending |
| ML dataset | In development |
| ML model | In development |
| Real mine validation | Future work |
| Automated alerts | Future work |

---

## Team Development

The repository is designed for collaborative development using Git and GitHub.

Suggested branch structure:

```text
main
|
├── feature/backend
├── feature/hardware
└── feature/ml
```

### Backend

Responsible for:

- Raspberry Pi
- Flask API
- SQLite
- Dashboard
- Risk engine
- Backend integration

### Hardware

Responsible for:

- Arduino Nano
- Sensor wiring
- Sensor acquisition
- Calibration
- Hardware testing

### Machine Learning

Responsible for:

- Dataset preparation
- Preprocessing
- Feature engineering
- Model training
- Model evaluation
- Prediction pipeline

---

## Prototype Disclaimer

Mine Monitor is an academic and research prototype.

It is not a certified mine-safety or structural-monitoring system.

Deployment in an operational mine would require appropriate sensor calibration, engineering validation, environmental testing, safety certification, reliable communication infrastructure, and validation against real mine conditions.

---

## Project Information

**Problem Statement:** SIH26025

**Project:** Development of an AI-enabled Low Cost Real Time Mine Subsidence Monitoring, Prediction and Early Warning System for Underground Coal Mines in India