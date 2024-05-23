void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n'); // Read the incoming data until newline character
    Serial.print("Received: ");
    Serial.println(received); // Print the received data
  }
  delay(1000); // Wait for a second before the next loop
}
