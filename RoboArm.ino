#include <stdlib.h>

//format [motor #][pwmA = 0, pwmB = 0]
const int MOTOR_PINS[5][2] = {{3,4}, {5,6}, {9, 10}, {23, 22}, {21, 20}};
const int SIGN = 1;
String msg = "";

void setup() {  
  Serial.begin(9600); //usb for testing
  Serial1.begin(9600);
}

void loop() {
  //check for inputs to bluetooth adapter
  while (Serial1.available()) {
   char reading = Serial1.read();
    if ((int)reading == 13 ) {
      Serial.println(msg);
      parseString(msg);
      msg = "";
    }
    else {
      msg += reading;
    }
  }
  
}

//motorSpeed should be between 0 and 1.0
void runMotor(int motorNum, double motorSpeed) {
  int pwmPin = 0;
  //deals with if we need to reverse directions from what is hooked up
  if (motorSpeed * SIGN < 0) {
    pwmPin = 1;
  }
  analogWrite(MOTOR_PINS[motorNum][pwmPin], motorSpeed * 255);
}

//motorNum, motorSpeed, duration (ms)
void parseString(String data) {
  int motorNum = int(data[0] - '0');
  int pos = 2;
  
  while (data[pos] != (int)' ') {
    pos++;
  } 
  double motorSpeed = atof(data.substring(2, pos).c_str());
  double duration = atof(data.substring(pos+1, data.length()).c_str());
  
  Serial.println(motorNum);
  Serial.println(motorSpeed);
  Serial.println(duration);
  Serial.println();
}
