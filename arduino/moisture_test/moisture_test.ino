const int MOISTURE_PIN = A6;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(MOISTURE_PIN);

  Serial.print("MOISTURE: ");
  Serial.println(value);

  delay(300);
}
