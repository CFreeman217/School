/*
 * Strain Gage Data Logging
 * 
 * Reads strain gage data from hx711 Load Cell Amplifier and writes to SD card module. 
 * 
 * TIME output given in milliseconds
 * OUTPUT given in read values between 0 and 16,777,215
 * 
 * HX711  -------  ARDUINO
 * GND                    GND
 * DT (Data)             A3
 * SCK (Serial Clock)  A2
 * VCC                     VCC (5V)
 * 
 * SD MODULE  ------  ARDUINO
 * GND                          GND
 * VCC                           VCC (5V)
 * MISO                          12
 * MOSI                          11
 * SCK                            13
 * CS                              4
 * 
 * Speed up or slow down sampling rate by changing the readsPerSec variable below.
 * Maximum sampling rate I have been able to achieve is around 10 samples per second.
 * This can be sped up by optimizing the SD card writing scheme
 * 
 */

#include <SPI.h>
#include <SD.h>
#include <Q2HX711.h>

const byte hx711_data_pin = A3;
const byte hx711_clock_pin = A2;
const int chipSelect = 4;
const int readingCount = 100;
const int readsPerSec = 1000;
const int readDelay = 10;
int readings[readingCount];

unsigned long previousMillis = 0;

Q2HX711 hx711(hx711_data_pin, hx711_clock_pin);

void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for native USB port only
//  }


  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
  Serial.println("TIME  ,  OUTPUT");
}

void loop() {
  unsigned long currentMillis = millis();
  String dataString = "";
  if (currentMillis - previousMillis >= 1000/readsPerSec) {
 
  
  // make a string for assembling the data to log:
  if (previousMillis == 0){
    dataString += " TIME  ,  OUTPUT ";
  } else {
  
  dataString += currentMillis;
  dataString += " , ";
  dataString += hx711.read();
  }

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("datalog.txt", O_CREAT | O_APPEND | O_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.println(dataString);
    dataFile.close();
    // print to the serial port too:
    Serial.println(dataString);

  }
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }
  }
  
  previousMillis = currentMillis;
}









