/*
* Arduino Wireless Communication Tutorial
*     Example 2 - Transmitter Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/

#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define DATARATE RF24_2MBPS

#define UPDN 14
#define LTRT 15

#define MAX_YAW_RATE 8
#define MAX_PITCH_DEGREES 10
// When joystick is centered, analog read input produces an offset of 1 to 2 degrees.
// this declaration establishes a floor to a joystick input to give to the controller
#define MIN_PITCH_DEGREES 3
#define MIN_YAW_RATE 2

RF24 radio(7, 8); // CE, CSN
const uint64_t pipes[2] = {000001,000002};
bool buttonState = 0;

typedef struct {
  int pitch;
  int yaw;
} commDef;

typedef struct {
  uint32_t timeytime;
  float des_ang;
  float meas_ang;
  float mot_cmd;
  float duty_cycle;
} FUCKINGDATA;

void setup() {
  pinMode(12, OUTPUT);
  Serial.begin(115200);
  radio.begin();
  radio.openWritingPipe(pipes[0]); // 00001
  radio.openReadingPipe(1, pipes[1]); // 00002
radio.setDataRate(DATARATE);
radio.setPALevel(RF24_PA_MAX);
radio.setChannel(0x34);
radio.powerUp();
radio.startListening();
}

void loop() {
  radio.startListening();
  if(radio.available()) {
    while(radio.available()) {
      FUCKINGDATA melvin;
      radio.read(&melvin, sizeof(melvin));
      Serial.print(melvin.timeytime);
      Serial.print(',');
      Serial.print(melvin.des_ang);
      Serial.print(',');
      Serial.print(melvin.meas_ang);
      Serial.print(',');
      Serial.print(melvin.mot_cmd);
      Serial.print(',');
      Serial.print(melvin.duty_cycle);
      Serial.println(',');
    }
  }
  
  commDef joystick;
  int raw_pitch = analogRead(UPDN);
   raw_pitch = map(raw_pitch, 0, 1023, -MAX_PITCH_DEGREES, MAX_PITCH_DEGREES);
    if(abs(raw_pitch) < MIN_PITCH_DEGREES) {
    raw_pitch = 0;
    }
  joystick.pitch = raw_pitch;
  int raw_yaw = analogRead(LTRT);
 raw_yaw = map(raw_yaw, 0, 1023, -MAX_YAW_RATE, MAX_YAW_RATE);
 if(abs(raw_yaw) < MIN_YAW_RATE) {
  raw_yaw = 0;
 }
 joystick.yaw = raw_yaw;
  radio.write(&joystick, sizeof(joystick));
  Serial.print(joystick.pitch);
  Serial.print(F(","));
  Serial.println(joystick.yaw);

}
