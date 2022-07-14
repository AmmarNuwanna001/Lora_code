/*
  This sample sketch demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
  Base on TinyGPSPlus //https://github.com/mikalhart/TinyGPSPlus
*/
#include <SPI.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include "utilities.h"
// For a connection via I2C using the Arduino Wire include:
#include <Wire.h>               // Only needed for Arduino 1.6.5 and earlier
#include "SSD1306Wire.h"        // legacy: #include "SSD1306.h"
// Optionally include custom images

#define SCK 5
#define MISO 19
#define MOSI 27
#define CS 18
#define RST 23
#define DIO0 26

//433E6 for Asia
//866E6 for Europe
//915E6 for North America
#define BAND 433E6

SSD1306Wire display(0x3c, I2C_SDA, I2C_SCL);

TinyGPSPlus gps;
int counter = 0;
void displayInfo();

void setup()
{
  initBoard();
  // When the power is turned on, a delay is required.
  delay(1500);
  Serial.begin(115200);
  Serial.println(F("DeviceExample.ino"));
  Serial.println(F("A simple demonstration of TinyGPS++ with an attached GPS module"));
  Serial.print(F("Testing TinyGPS++ library v. "));
  Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println(F("by Mikal Hart"));
  Serial.println();

  // Initialising the UI will init the display too.
  display.init();

  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);

  Serial.println("LoRa Sender Test");

  //SPI LoRa pins
  SPI.begin(SCK, MISO, MOSI, SS);
  //setup LoRa transceiver module
  LoRa.setPins(CS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("LoRa Initializing OK!");
  delay(2000);
}


void loop()
{
  display.clear();

  // This sketch displays information every time a new sentence is correctly encoded.
  while (Serial1.available() > 0)
    if (gps.encode(Serial1.read()))
      displayInfo();

  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }
  //Send LoRa packet to receiver
}

void displayInfo()
{
  Serial.print(F("Location: "));
  if (gps.location.isValid()) {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
    display.drawString(0, 0, String(gps.location.lat()));
    display.drawString(0, 10, String(gps.location.lng()));
    LoRa.beginPacket();
    LoRa.print("33175552-d263-49da-8c37-cf7366b4d8d5,");//timestamp,GUID,Lat,Long,RSSI
    LoRa.print(gps.location.lat(), 6);
    LoRa.print(",");
    LoRa.print(gps.location.lng(), 6);
    LoRa.print(counter);
    LoRa.endPacket();
    counter++;
    delay(10000);
  } else {
    display.drawString(0, 10, "INVALID Location");
    LoRa.beginPacket();
    LoRa.print("33175552-d263-49da-8c37-cf7366b4d8d5,Invalid location");
    LoRa.print(",test,test");
    LoRa.print(counter);
    LoRa.endPacket();
    counter++;
    delay(10000);
  }

//  Serial.print(F("  Date/Time: "));
//  if (gps.date.isValid()) {
//    Serial.print(gps.date.month());
//    Serial.print(F("/"));
//    Serial.print(gps.date.day());
//    Serial.print(F("/"));
//    Serial.print(gps.date.year());
//  } else {
//    Serial.print(F("INVALID"));
//    display.drawString(0, 10, "INVALID Date");
//  }
//
//  Serial.print(F(" "));
//  if (gps.time.isValid()) {
//    if (gps.time.hour() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.hour());
//    Serial.print(F(":"));
//    if (gps.time.minute() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.minute());
//    Serial.print(F(":"));
//    if (gps.time.second() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.second());
//    Serial.print(F("."));
//    if (gps.time.centisecond() < 10) Serial.print(F("0"));
//    Serial.print(gps.time.centisecond());
//  } else {
//    Serial.print(F("INVALID"));
//    display.drawString(0, 20, "INVALID Time");
//  }

  Serial.println();


  display.display();
}