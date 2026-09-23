\# Mine Monitor



\### AI-Enabled Real-Time Mine Subsidence Monitoring \& Early Warning System



> \*\*SIH26025 — Smart India Hackathon Project\*\*



Mine Monitor is a low-cost prototype designed to continuously monitor environmental and structural parameters in underground coal-mine environments and provide real-time risk assessment and early warning.



The system combines multiple sensors, an Arduino Nano, Raspberry Pi, SQLite, a Flask dashboard, and a machine-learning pipeline.



\---



\## 🎯 Project Objective



Underground mine subsidence can develop due to changes in structural loading, deformation, roof convergence, ground conditions, and other environmental factors.



The objective of Mine Monitor is to:



\- Collect multiple sensor readings in real time.

\- Store and organize sensor data.

\- Monitor structural and environmental changes.

\- Combine multiple sensor parameters for risk assessment.

\- Provide a real-time monitoring dashboard.

\- Generate early warnings when abnormal conditions are detected.

\- Provide a foundation for machine-learning-based subsidence prediction.



> \*\*Note:\*\* This repository contains a prototype system. Sensor values and risk thresholds require calibration and validation using appropriate engineering measurements and real mine/field data before deployment.



\---



\## 🏗️ System Architecture



```text

┌───────────────────────────────┐

│          Sensors              │

│                               │

│ MQ-4 | ADXL335 | FSR | Flex  │

│ HC-SR04 | Moisture Sensor     │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               ▼

┌───────────────────────────────┐

│        Arduino Nano           │

│                               │

│ Sensor acquisition            │

│ Analog-to-digital conversion  │

│ Basic data formatting         │

└───────────────┬───────────────┘

&#x20;               │ USB Serial

&#x20;               ▼

┌───────────────────────────────┐

│        Raspberry Pi 4         │

│                               │

│ Serial data acquisition       │

│ Data validation               │

│ Risk engine                   │

│ Flask API                     │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               ▼

┌───────────────────────────────┐

│          SQLite               │

│                               │

│ Timestamped sensor records    │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               ▼

┌───────────────────────────────┐

│      Flask Web Dashboard      │

│                               │

│ Live sensor values            │

│ Risk score                    │

│ Risk level                    │

│ System status                 │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               ▼

┌───────────────────────────────┐

│       ML / Risk Engine        │

│                               │

│ Feature engineering           │

│ Model prediction              │

│ Early warning                 │

└───────────────────────────────┘

