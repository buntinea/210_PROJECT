#include <Wire.h>

const int ledPin = 13;

void setup() {
  Wire.begin(0x1);

  Wire.onReceive(receiveEvent);

  pinMode(ledPin,OUTPUT);
  digitalWrite(ledPin,LOW);

}

void receiveEvent(int howMany){
  while(Wire.available()){
    char c = Wire.read();
    flashLED();
    digitalWrite(ledPin, c);
  }
}

void loop(){
  delay(100);
}

void flashLED(){
  digitalWrite(ledPin,LOW);
  delay(500);
  digitalWrite(ledPin,HIGH);
  delay(500);
  digitalWrite(ledPin,LOW);
  delay(500);
  digitalWrite(ledPin,HIGH);
  delay(500);
  digitalWrite(ledPin,LOW);
  delay(500);
  digitalWrite(ledPin,HIGH);
  delay(500);
  digitalWrite(ledPin,LOW);
}
