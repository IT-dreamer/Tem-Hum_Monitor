#include <dht11.h>
#define DHT11_PIN 4
#define LED_PIN 13
#define FAN_PIN 8

dht11 DHT;
void setup(){
  Serial.begin(9600);
  pinMode(LED_PIN,OUTPUT);
  pinMode(DHT11_PIN,OUTPUT);
  pinMode(FAN_PIN,OUTPUT);
}

void loop(){
  int chk;
  chk = DHT.read(DHT11_PIN); 
  delay(2000);
  if(chk== DHTLIB_OK){
    Serial.print("humidity:");
    Serial.print(DHT.humidity);
    Serial.print("%  ");
    Serial.print("temperature:");
    Serial.print(DHT.temperature);
    Serial.println("*C");
  }
  if(DHT.humidity>=42||DHT.temperature>=25){
    digitalWrite(LED_PIN,HIGH);
    delay(1000);
    digitalWrite(LED_PIN,LOW);
    delay(1000);
    digitalWrite(FAN_PIN,HIGH);
    }
   else digitalWrite(FAN_PIN,LOW);
  delay(1000);
}
