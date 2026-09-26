const int FSR_PIN = A4;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(FSR_PIN);

  Serial.print("FSR: ");
  Serial.println(value);

  delay(200);
}
