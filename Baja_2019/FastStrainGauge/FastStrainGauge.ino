//SD.h 
//#include <SPI.h>
//#include <SD.h>
//File dataFile;

//SdFat.h 
#include <SPI.h>
#include <SdFat.h>
SdFat sd;
SdFile dataFile;

const byte CS_PIN  = 4;
const byte analogPin0 = A0;   
const byte analogPin1 = A1;   
const byte analogPin2 = A2; 
const char filename[] = "ArduinoPoop_7.csv";
int val = 0; 

void setup () {
//  Serial.begin(115200);
//  Serial.println("Type any Character to begin");
//  while (Serial.read() <= 0) { }

//  Serial.println("Initializing Card");
  pinMode(CS_PIN, OUTPUT);
 
  if (!sd.begin(CS_PIN))//SdFat.h syntax
//  if(!SD.begin(CS_PIN))//SD.h syntax
  {
//    Serial.println("Card Failure");
    while(1);
  }
//  Serial.println("Card Ready");

  if (dataFile.open(filename, O_RDWR | O_CREAT | O_AT_END)) //SdFat syntax
   
//    dataFile = SD.open("ConstantWriteTest.csv",FILE_WRITE);//SD.h
//    if(dataFile)//Sd.h
  {
//    Serial.println("data file open");
    dataFile.println(F("n_point, Pin A0, Pin A1, Pin A2, Current Time(ms), Time since last write (us)"));
  }
  else
  {
//    Serial.println("error opening file");
    while(1);
  }
}

void loop () { 
 
  static unsigned long recordNumber=0;
  static unsigned long lastWrite = micros();
  dataFile.print(recordNumber++);
  dataFile.print(",");
  dataFile.print(analogRead(analogPin0));
  dataFile.print(",");
  dataFile.print(analogRead(analogPin1));
  dataFile.print(",");
  dataFile.print(analogRead(analogPin2));
  dataFile.print(",");
  dataFile.print(millis());
  dataFile.print(",");
  dataFile.println(micros() - lastWrite);
  lastWrite = micros();


  // Save data after 5 minutes
  static unsigned long chunkTime = 300000;
  static unsigned long startLog = millis();
  
  
  if ((millis() - startLog) > chunkTime) {
    dataFile.close();
//    Serial.println("close file");
    if (dataFile.open(filename, O_RDWR | O_CREAT | O_AT_END)) //SdFat syntax
   
//    dataFile = SD.open("ConstantWriteTest.csv",FILE_WRITE);//SD.h
//    if(dataFile)//Sd.h
  {
//    Serial.println("data file open");
    startLog += chunkTime;
  }
  else
  {
//    Serial.println("error opening file");
    while(1);
  }
}
}
