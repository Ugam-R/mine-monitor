const int MQ4_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(MQ4_PIN);

  Serial.print("MQ4: ");
  Serial.println(value);

  delay(500);
}
