#include <stdlib.h>

IntervalTimer myTimer;

//format [motor #][pwmA = 0, pwmB = 0]
const int MOTOR_PINS[5][2] = {{9, 10}, {6,5}, {20, 21}, {22, 23}, {4, 3}};
const int SIGN = 1;

const int MOVE_DURATION = 50; //ms

String msg = "";

//format motorvals: [motorPwmPin, motorSpeed, duration]
int motorPwmPins[5] = {0};
double motorSpeeds[5] = {0};
int durations[5] = {0};

void setup() {  
  Serial1.begin(9600);
  myTimer.begin(doMotors, 1000);  //timed interrupt for every 1 ms
}

void loop() {
  //check for inputs to bluetooth adapter
 while (Serial1.available()) {

   char reading = Serial1.read();
    if ((int)reading == (int) '\n' ) {
      parseString(msg);
      msg = "";
    }
    else {
      msg += reading;
    }
  }  
}

//motorSpeed should be between -1.0 and 1.0
//duration in ms
void setMotorVals(int motorNum, double motorSpeed, int duration) {
  int pwmPin = 0;
  if (abs(motorSpeed) > 1) motorSpeed = motorSpeed/abs(motorSpeed);
  //deal with if we need to reverse directions from what is hooked up
  if (motorSpeed * SIGN < 0) {
    pwmPin = 1;
  }
  motorPwmPins[motorNum] = MOTOR_PINS[motorNum][pwmPin];
  analogWrite(MOTOR_PINS[motorNum][(pwmPin + 1)%2], 0);  //write the opposite pwm pin to 0 to prevent shorts
  motorSpeeds[motorNum] = abs(motorSpeed);
  durations[motorNum] = duration;
  
}

void doMotors() {
  for (int i = 0; i < 5; i++) {
    if (durations[i] > 0) {  //duration > 0
    /*
    Uncomment for real tests
    */
    analogWrite(motorPwmPins[i], (int) (motorSpeeds[i] * 255));  //pwmPin, motorSpeed
    
      durations[i]--; //duration
      if (durations[i] <= 0) analogWrite(motorPwmPins[i], 0);
    }
    else durations[i] = 0;
  }
}

//motorNum, motorSpeed, duration (ms)
void parseString(String data) {
  int motorNum = (data[0] - '0');
  double motorSpeed = atof(data.substring(1, data.length()).c_str());
  
   setMotorVals(motorNum, motorSpeed, MOVE_DURATION);
}
