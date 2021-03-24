/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-temperature-humidity-sensor
 */

#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
#define buffer 50

DHT dht(DHTPIN, DHTTYPE);


int index = 0;
float last[buffer];

void setup() {
  Serial.begin(9600);
  dht.begin(); // initialize the sensor
}

void loop() {
  // wait a few seconds between measurements.
  if(index < buffer) {
    delay(1000);
  } else {
    delay(2000); 
  }

  // read humidity
  float humi  = dht.readHumidity();
  float temp  = dht.readTemperature();

  // check if any reads failed
  if (isnan(humi)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    last[index%buffer] = humi;
    index++;
    
    

    if (index > buffer) {
      Serial.print(", ");
      Serial.print(humi);
      Serial.print(", ");
      Serial.print(avg(last));
      Serial.print(", ");
      Serial.print(temp);
      Serial.print("");
  
      if (humi + 3 <= avg(last)) {
        Serial.println(",1");
      } else {
        Serial.println(",0");
      }
    }
  }
}

float avg(float arr[]) {
  float sum = 0;
  for (int i = 0; i < buffer; i++) {
    sum += arr[i];
  }
  return sum/buffer;
}
