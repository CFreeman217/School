
#include <MPU6050_tockn.h>
#include <Wire.h>
//#include <math.h>

#define sampFreq 100
#define cutoffFreq 1
#define math_PI 3.14159

#define controlPin1 4
#define controlPin2 3
#define enablePin 9

#define K_p 30
#define K_i 40
#define K_d 0.5


int motorDirection = 0;
float max_lambda = 0;
float pitch_d = 0;
float err_p_old, err_r_old, err_y_old = 0;

MPU6050 mpu6050(Wire);

long timer = 0;

void setup() {
  //Serial.begin(9600);
  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  pinMode(controlPin1, OUTPUT);
  pinMode(controlPin2, OUTPUT);
  pinMode(enablePin, OUTPUT);
  //digitalWrite(enablePin,LOW);
}
/*
//-------------------- BUTTERWORTH FILTERING --------------------
float x_n1, x_n2, y_n1, y_n2 = 0;
float butter2(float in_data, bool highPass) {
  /*
   * 2nd order butterworth filter for high or low pass data filtering
   */
  /*
  float f_c = cutoffFreq;
  float f_s = sampFreq;
  float math_pi = 355/113; // approximation of pi
  
  float gam = tan((math_pi*f_c) / f_s);
  float coef_d = pow(gam, 2) + pow(2, 0.5) * gam +1;
  float a_1 = (2 * (pow(gam, 2) - 1)) / coef_d;
  float a_2 = (pow(gam, 2) - pow(2, 0.5) * gam + 1)/ coef_d;
  float b_0, b_1, b_2;
  if(highPass == true){
    b_0 = 1;
    b_1 = -2;
    b_2 = b_0;
    } else {
    b_0 = (pow(gam, 2))/coef_d;
    b_1 = (2 * b_0) / coef_d;
    b_2 = b_0;  
    }
  float y_n = b_0 * in_data + b_1 * x_n1 + b_2 * x_n2 - a_1 * y_n1 - a_2 * y_n2;
  x_n2 = x_n1;
  x_n1 = in_data;
  y_n2 = y_n1;
  y_n1 = y_n;
  return (y_n);
}
*/

void setMotor(int speed, bool reverse)
{
  analogWrite(enablePin, speed);
  digitalWrite(controlPin1, ! reverse);
  digitalWrite(controlPin2, reverse);
}
void loop() {
  
  if(millis() - timer > (1000/sampFreq)){
    mpu6050.update();
    float pitch_m = mpu6050.getAngleX();
    //Serial.print("Measured Pitch : "); Serial.print(pitch_m);
    float err_pp = pitch_d - pitch_m;
    float err_pi = (err_pp + err_p_old)/(2* sampFreq);
    float err_pd = (err_pp - err_p_old)*sampFreq;
    float lambda_p = (err_pp*K_p) + (err_pi*K_i) + (err_pd*K_d);
    bool mot_dir;
    err_p_old = err_pp;
    if(lambda_p > 0) {
      mot_dir = true;
      //Serial.print("\tMotor Clockwise");
    } else {
      mot_dir = false;
      //Serial.print("\tMotor Counter-Clockwise");
    }
    if(fabs(lambda_p) > max_lambda) {max_lambda = fabs(lambda_p);}
    int m_cmd = map(fabs(lambda_p), 0, max_lambda, 0, 255);
    if(m_cmd > 255) {m_cmd = 255;}
    //Serial.print("\tLambda = ");Serial.print(lambda_p);
    //Serial.print("\tMotor Command = ");Serial.println(m_cmd);
    setMotor(m_cmd, mot_dir);
    timer = millis();
    
  }

}
