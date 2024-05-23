#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;

void setup() {
  Serial.begin(115200); // Start serial communication
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
}

void parseCoordinates(String message, int &destX, int &destY, int &ballX, int &ballY) {
  int firstColon = message.indexOf(':');
  int firstSlash = message.indexOf('/');
  int secondColon = message.indexOf(':', firstSlash);
  int secondSlash = message.indexOf('/', secondColon);
  int thirdColon = message.indexOf(':', secondSlash);
  int thirdSlash = message.indexOf('/', thirdColon);
  int fourthColon = message.indexOf(':', thirdSlash);
  int newline = message.indexOf('\n');

  destX = message.substring(firstColon + 1, firstSlash).toInt();
  destY = message.substring(secondColon + 1, secondSlash).toInt();
  ballX = message.substring(thirdColon + 1, thirdSlash).toInt();
  ballY = message.substring(fourthColon + 1, newline).toInt();
}

void loop() {
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n'); // Read the incoming data until newline character
    int destX = 0, destY = 0, ballX = 0, ballY = 0;
    parseCoordinates(received, destX, destY, ballX, ballY);

    Serial.print("Received: ");
    Serial.print("destX: ");
    Serial.print(destX);
    Serial.print(", destY: ");
    Serial.print(destY); 
    Serial.print(", ballX: ");
    Serial.print(ballX);
    Serial.print(", ballY: ");
    Serial.println(ballY); 
  }




  
}
