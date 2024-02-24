#include <DFRobotDFPlayerMini.h>
#include <SoftwareSerial.h>
#include <SPI.h>
#include <Adafruit_I2CDevice.h>
#include "RTClib.h"

int x;
const byte rxPinDfplayer = 2;
const byte txPinDfplayer = 3;
const byte txPinLora = 10;
const byte rxPinLora = 11;
const int pinLedKuning = 4;
const int pinLedMerah = 12;
const int pinLedBiru = 9;
const int pinLedHijau = 13;

SoftwareSerial lora(txPinLora, rxPinLora);
SoftwareSerial dfplayer(rxPinDfplayer, txPinDfplayer);
DFRobotDFPlayerMini myDFPlayer;
RTC_DS3231 rtc;

char daysOfTheWeek[7][12] = {"Ahad", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

void setup()
{

  Serial.begin(9600);
  dfplayer.begin(9600);
  lora.begin(9600);
  Serial.setTimeout(1);
  myDFPlayer.begin(dfplayer);
  // myDFPlayer.volume(40);
  // myDFPlayer.play(2);
  // myDFPlayer.read();

  if (!rtc.begin())
  {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1)
      delay(10);
  }

  if (rtc.lostPower())
  {
    Serial.println("RTC lost power, let's set the time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  pinMode(rxPinDfplayer, INPUT);
  pinMode(txPinDfplayer, OUTPUT);
  pinMode(pinLedKuning, OUTPUT);
  pinMode(pinLedMerah, OUTPUT);
  pinMode(pinLedHijau, OUTPUT);
  pinMode(pinLedBiru, OUTPUT);

  digitalWrite(pinLedKuning, HIGH);
  digitalWrite(pinLedMerah, HIGH);
  digitalWrite(pinLedHijau, HIGH);
  digitalWrite(pinLedBiru, HIGH);
  delay(1000);
}

void loop()
{

  digitalWrite(pinLedKuning, LOW);
  digitalWrite(pinLedHijau, HIGH);

  DateTime now = rtc.now();
  Serial.print(";");
  Serial.print("on_time");
  Serial.print(";");
  Serial.print(now.year(), DEC);
  Serial.print('_');
  Serial.print(now.month(), DEC);
  Serial.print('_');
  Serial.print(now.day(), DEC);
  Serial.print(";");
  Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
  Serial.print(";");
  Serial.print(now.hour(), DEC);
  Serial.print('_');
  Serial.print(now.minute(), DEC);
  Serial.print('_');
  Serial.print(now.second(), DEC);
  Serial.print(";");
  Serial.println();

  delay(100);

  // while (!Serial.available())
  //   ;
  x = Serial.readString().toInt();
  if (x == 1)
  {
    myDFPlayer.play(2);
    myDFPlayer.read();
    digitalWrite(pinLedHijau, LOW);
    digitalWrite(pinLedKuning, HIGH);
    lora.println("Data Dari Kamera");
    delay(6000);
    digitalWrite(pinLedHijau, LOW);
    digitalWrite(pinLedKuning, LOW);
  }
}
