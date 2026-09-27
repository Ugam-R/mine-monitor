const int FLEX_PIN = A5;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int value = analogRead(FLEX_PIN);

  Serial.print("FLEX: ");
  Serial.println(value);

  delay(200);
}
