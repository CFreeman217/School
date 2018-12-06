/*
 * Wheelie Bot: VERSION 2 - NDI
 * 
 * Controller for arduino powered two wheeled robot using nonlinear dynamic inversion
 * 
 * Equation of motion:
 * 
 * F = [x_2d]*(M + m) - mL[phi_2d]*cos(phi) + mL[phi_1d]^2*sin(phi)
 * 
 * Sum of moments about pivot point:
 * 
 * T + mgL*sin(phi) = [phi_2d]*(I_g + mL^2) - mL[x_2d]*cos(phi)
 * 
 * LET:
 * F = horizontal force to keep robot standing (N)
 * T = motor torque (1 oz-in = 13.887386 kg-cm)
 * m = mass of body (kg)
 * M = mass of body + wheels (kg)
 * L = distance to body center of gravity (m)
 * I_g = moment of inertia about pivot point (kg-m^2)
 * g = gravitational (vertical) acceleration (9.81 m/s^2)
 * [x_2d] = horizontal acceleration (m/s^2)
 * phi = angle away from vertical (rad)
 * [phi_1d] = angular velocity from vertical (rad/s)
 * [phi_2d] = angular acceleration from vertical (rad/s^2)
 * 
 * Control Law:
 * 
 * [phi_2d] = [phi_2desired] + k_1*([phi_1desired] - [phi_1d]) + k_2*([phi_desired] - phi)
 * 
 * Rearranging moment equation and control law for [phi_2d]
 * 
 * T - [phi_2d]*(I_g + mL^2) + mL*([x_2d]*cos(phi) + g*sin(phi)) = [phi_2desired] + k_1*([phi_1desired] - [phi_1d]) + k_2*([phi_desired] - phi)
 * 
 * Simplify by assuming [phi_2desired] = [phi_1desired] = 0 
 * 
 * Solve for T which becomes the motor command
 * 
 * T = k_2*([phi_desired] - phi) - k_1*[phi_1d] + [phi_2d]*(I_g + mL^2) - mL*([x_2d]*cos(phi) + g*sin(phi))
 * 
 * SETUP Rev 1:
 * 
 * MPU6050 -> Arduino
 * Vcc -> 5v
 * GND
 * SCL -> Pin A5
 * SDA -> Pin A4
 * INT -> Pin 2
 * 
 * NRF24L01 Radio -> Arduino
 * Pin 1 - GND
 * Pin 2 - CE    -> Pin 7
 * Pin 3 - SCK   -> Pin 13
 * Pin 4 - MISO  -> Pin 12
 * Pin 5 - IRQ   -> NC
 * Pin 6 - MOSI  -> Pin 11
 * Pin 7 - CSN   -> Pin 8
 * Pin 8 - 3v3 (5v if using radio helper block)
 * 
 */

// Libraries to communicate with MPU
#include <MPU6050_tockn.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h>

#define w_n 4 // Increase for faster response time
#define zeta 1 // Decrease if model is less accurate, 1 = no overshoot

#define m_a 0.5 // Mass of body arm (kg)
#define L_a 0.05 // Length to center of gravity (m)
#define Ig_a 0.8 // Moment of intertia for arm about pivot point (kg-m^2)

#define stp 100 // sampling rate (Hz)
#define MAX_ANGLE 20 // Maximum Angle (degrees)

#define LMD 6 // Left Motor Direction Pin
#define LMS 3 // Left Motor Speed Pin (PWM)
#define RMD 9 // Right Motor Direction Pin 
#define RMS 5 // Right Motor Speed Pin (PWM)


// Define transmission datarate for NRF24L01
#define DATARATE RF24_2MBPS

// Instantiate the communication radio
RF24 radio(7,8); // CE, CSN
const uint64_t pipes[2] = {000001,000002};

// Instantiate the MPU
MPU6050 mpu6050(Wire);
// The MPU I got from amazon FUCKING SUCKS ASS, so I need to waste precious variable space on offset calculations in setup
float X_offset;
float Y_offset;
float Z_offset;
float X_acc_offset;
float Y_acc_offset;
float Z_acc_offset;

// Communication definition structure for sending data through radio
typedef struct {
  int pitch;
  int yaw;
} commDef;

long timer; // Tracks clock for state update
float theta_des = 0; // Desired angle

//float pitch_cmd_max = 1; // maximum value from NDI calculation
float theta_prev1 =0; // Previous angle measurement
float theta_prev2 =0; // Angle measurement from 2 cycles ago

void setMotor(float pit_cmd, float yaw_cmd, int lm_dir, int lm_pwm, int rm_dir, int rm_pwm, int max_theta) {
  /*
   * Sets motor commands and writes appropriate output to pins.
   * 
   * pit_cmd = pitch command to maintain balance and keep direction
   * yaw_cmd = yaw command to turn the bot
   * 
   * lm_dir = pin to determine the motor direction for the left motor
   * lm_pwm = pin that gets the desired motor speed command
   * 
   * rm_dir = pin to determin the motor direction for the right motor
   * rm_pwm = pin that gets the desired motor speed command
   */
   float lambda_L;
   float lambda_R;
   // Determine overall forward or backward command with the turning command
  if(yaw_cmd > 0) {
    lambda_L = pit_cmd + yaw_cmd;
    lambda_R = pit_cmd - yaw_cmd;
  } else {
    lambda_L = pit_cmd - yaw_cmd;
    lambda_R = pit_cmd + yaw_cmd;
  }
  if(lambda_L > 0) {
    digitalWrite(lm_dir, HIGH);
  } else {
    digitalWrite(lm_dir, LOW);
  }
  if(lambda_R > 0) {
    digitalWrite(rm_dir, HIGH);
  } else {
    digitalWrite(rm_dir, LOW);
  }
   lambda_L = map(abs(lambda_L), 0, max_theta, 0, 255);
   lambda_R = map(abs(lambda_R), 0, max_theta, 0, 255);
   analogWrite(lm_pwm, lambda_L);
   analogWrite(rm_pwm, lambda_R);
}

// Numeric differentiation for first derivative by backward finite divided difference
float dot(float curr, float prev, float hgt) {
return((curr - prev) / hgt);
}

// Numeric differentiation for second derivative by backward finite divided difference
float dbl_dot(float curr, float prev1, float prev2, float hgt) {
return((curr - 2*prev1 + prev2) / hgt);
}

// Setup initialization commands
void setup() {
Serial.begin(115200);
radio.begin();
//radio.openWritingPipe(addresses[0]); // 000001
radio.openReadingPipe(1,pipes[0]); // 000002
radio.setDataRate(DATARATE);
radio.setPALevel(RF24_PA_MAX);
radio.setChannel(0x34);
//radio.setAutoAck( true );
//radio.printDetails();
radio.powerUp();
radio.startListening();

Wire.begin();
mpu6050.begin();
mpu6050.calcGyroOffsets(true);
mpu6050.update();
X_offset = mpu6050.getAngleX();
Y_offset = mpu6050.getAngleY();
Z_offset = mpu6050.getAngleZ();
X_acc_offset = mpu6050.getAccX();
Y_acc_offset = mpu6050.getAccY();
Z_acc_offset = mpu6050.getAccZ();
}

// Main program
void loop() {
  int yaw_des = 0;
  radio.startListening();
  if(radio.available()) {
  while(radio.available()) {
    commDef joystick;
    radio.read(&joystick, sizeof(joystick));
    theta_des = joystick.pitch;
    }
  }
  if(millis() - timer > (1000/stp)) {
  // Update the MPU measurements
      mpu6050.update();
      float theta_meas = (mpu6050.getAngleX()-X_offset)*(PI/180); // current measured angle
      float theta_dot = dot(theta_meas, theta_prev1,1/stp); // calculated angular rate
      float theta_dbl_dot = dbl_dot(theta_meas, theta_prev1, theta_prev2, 1/stp); // calculated angular acceleration
      float x_dbl_dot = (mpu6050.getAccX() - X_acc_offset)*9.81; // measured x-acceleration
      float z_dbl_dot = (mpu6050.getAccZ() - Z_acc_offset)*9.81; // measured z-acceleration
      float k_1 = 2*zeta*w_n; // Knowledge of system
      float k_2 = w_n*w_n; // Controller response time
      // Compute torque command to be sent to motor
      float pitch_cmd = k_2*(theta_des - theta_meas) - k_1*theta_dot + theta_dbl_dot*(Ig_a + m_a*L_a*L_a) - m_a*L_a*(x_dbl_dot*cos(theta_meas) + z_dbl_dot*sin(theta_meas));
      setMotor(pitch_cmd, yaw_des, LMD, LMS, RMD, RMS, k_2*MAX_ANGLE*PI/180);
      // Cycle variables used for tracking derivatives
      theta_prev2 = theta_prev1;
      theta_prev1 = theta_meas;
//      Serial.println(t_cmd);
      timer = millis();
    } 
}
