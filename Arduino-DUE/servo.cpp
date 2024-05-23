#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the incoming data until newline character
    int commaIndex1 = command.indexOf(',');
    int commaIndex2 = command.lastIndexOf(',');

    if (commaIndex1 > 0 && commaIndex2 > commaIndex1){
      int servo1_angle = command.substring(0, commaIndex1).toInt();
      int servo2_angle = command.substring(commaIndex1 + 1, commaIndex2).toInt();
      int servo3_angle = command.substring(commaIndex2 + 1).toInt();

      servo1.write(servo1_angle);
      servo2.write(servo2_angle);
      servo3.write(servo3_angle);

      Serial.print("Servo posities ingesteld op: ");
      Serial.print(servo1_angle);
      Serial.print(", ");
      Serial.print(servo2_angle);
      Serial.print(", ");
      Serial.println(servo3_angle);
    }
  }
}
