#include <Servo.h>

Servo servo1; // Top right corner
Servo servo2; // Top left corner
Servo servo3; // Middle bottom

// PID constants
float Kp = 0.5;
float Kd = 0.55;
float Ki = 0.08;


// PID variables
float previousErrorX = 0;
float previousErrorY = 0;
float integralX = 0;
float integralY = 0;

unsigned long lastTime;

void setup() {
  Serial.begin(115200); // Start serial communication
  servo1.attach(10); 
  servo2.attach(9);
  servo3.attach(11);

  // Initialize servos to 90 degrees (resting position)
  servo1.write(90);
  servo2.write(90);
  servo3.write(90);

  lastTime = millis(); // Initialize lastTime for PID calculations
}

// Coords format
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

// PID controller
void PIDControl(int destX, int destY, int ballX, int ballY) {
  unsigned long currentTime = millis();
  float elapsedTime = (currentTime - lastTime) / 1000.0; // Calculate elapsed time in seconds

  // Calculate the error terms
  float errorX = destX - ballX;
  float errorY = destY - ballY;

  // Integral term
  integralX += errorX * elapsedTime;
  integralY += errorY * elapsedTime;

  // Derivative term
  float derivativeX = (errorX - previousErrorX) / elapsedTime;
  float derivativeY = (errorY - previousErrorY) / elapsedTime;

  // PID output
  float outputX = Kp * errorX + Ki * integralX + Kd * derivativeX;
  float outputY = Kp * errorY + Ki * integralY + Kd * derivativeY;

  // Calculate servo angles based on PID output
  updateServos(outputX, outputY);

  // Save the current error as the previous error for the next iteration
  previousErrorX = errorX;
  previousErrorY = errorY;
  lastTime = currentTime;
}

void updateServos(float outputX, float outputY) {
  // Calculate the servo positions based on the PID outputs
  // These calculations will need to be adjusted based on your setup
  // Here, we assume a simple linear relationship between the output and the servo position

  // Example calculations (these will need to be adjusted based on your setup)
  int servoPos1 = constrain(map(outputY + outputX, -100, 100, 90, 120), 90, 120); // Top right
  int servoPos2 = constrain(map(outputY - outputX, -100, 100, 90, 120), 90, 120); // Top left
  int servoPos3 = constrain(map(-outputY, -100, 100, 90, 120), 90, 120); // Middle bottom

  // Update the servo positions
  servo1.write(servoPos1);
  servo2.write(servoPos2);
  servo3.write(servoPos3);
}

void loop() {
  if (Serial.available() > 0) {
    String received = Serial.readStringUntil('\n'); // Read the incoming data until newline character
    Serial.print("Raw received: ");
    Serial.println(received); // Debugging: Print the raw received string

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

    // Call the PID controller
    PIDControl(destX, destY, ballX, ballY);
  }
}
