// ======================================================
// SMART MINE SUBSIDENCE MONITORING - SENSOR NODE
// Arduino Nano
// ======================================================

const int MQ4_PIN = A0;

const int ADXL_X_PIN = A1;
const int ADXL_Y_PIN = A2;
const int ADXL_Z_PIN = A3;

const int FORCE_PIN = A4;
const int FLEX_PIN = A5;
const int MOISTURE_PIN = A6;

const int TRIG_PIN = 2;
const int ECHO_PIN = 3;

const int BUZZER_PIN = 4;

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(BUZZER_PIN, LOW);
}

float readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duration == 0) {
    return -1;
  }

  float distance = duration * 0.0343 / 2.0;

  return distance;
}

void loop() {

  // Read sensors
  int methaneRaw = analogRead(MQ4_PIN);

  int accelX = analogRead(ADXL_X_PIN);
  int accelY = analogRead(ADXL_Y_PIN);
  int accelZ = analogRead(ADXL_Z_PIN);

  int forceRaw = analogRead(FORCE_PIN);
  int flexRaw = analogRead(FLEX_PIN);

  int moistureRaw = analogRead(MOISTURE_PIN);

  float roofDistance = readDistanceCM();

  // Send structured data to Raspberry Pi
  Serial.print("{");

  Serial.print("\"methane_raw\":");
  Serial.print(methaneRaw);

  Serial.print(",\"accel_x\":");
  Serial.print(accelX);

  Serial.print(",\"accel_y\":");
  Serial.print(accelY);

  Serial.print(",\"accel_z\":");
  Serial.print(accelZ);

  Serial.print(",\"force_raw\":");
  Serial.print(forceRaw);

  Serial.print(",\"flex_raw\":");
  Serial.print(flexRaw);

  Serial.print(",\"moisture_raw\":");
  Serial.print(moistureRaw);

  Serial.print(",\"roof_distance_cm\":");
  Serial.print(roofDistance);

  Serial.println("}");

  delay(1000);
}
