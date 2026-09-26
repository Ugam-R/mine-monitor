const int X_PIN = A1;
const int Y_PIN = A2;
const int Z_PIN = A3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int x = analogRead(X_PIN);
  int y = analogRead(Y_PIN);
  int z = analogRead(Z_PIN);

  Serial.print("X: ");
  Serial.print(x);

  Serial.print("  Y: ");
  Serial.print(y);

  Serial.print("  Z: ");
  Serial.println(z);

  delay(200);
}
