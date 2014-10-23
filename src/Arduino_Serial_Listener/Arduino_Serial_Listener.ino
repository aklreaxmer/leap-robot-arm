#include <Servo.h> 

Servo bottom;
Servo middle;
Servo claw;

int minPulse = 600; 
int maxPulse = 2400; 

int serialIn[3];    
int startbyte;       
int servo;         
int pos;

void setup() 
{ 
  bottom.attach(10, minPulse, maxPulse);
  middle.attach(9, minPulse, maxPulse);
  claw.attach(8, minPulse, maxPulse);
 
  Serial.begin(9600);
} 

void loop() 
{ 
  //receive data from python script
  if (Serial.available() > 2) { 
        //script sends 3 bytes, so check if 3 bytes are available
    byte b = Serial.read();
    if (b == -1) //check for start byte
    {
      Serial.readBytes(serialIn, 2); //get the servo and angle
      servo = serialIn[0];
      angle = serialIn[1];
    
      if(servo == 1) //write to appropriate servo
        bottom.write(100 - angle);
      if(servo == 2)
        middle.write(angle);
      if(servo == 3)
        claw.write(angle);
      }
      delay(5);
    }
  }
}
