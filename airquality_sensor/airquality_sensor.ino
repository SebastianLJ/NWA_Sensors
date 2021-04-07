/*
 * Data will come out on serial monitor in following format
 * humidity, avg. humidity, temperature, isWindowOpen(0/1), CO2, tVOC
 */

#include <Wire.h>
#include "SparkFunCCS811.h" //Click here to get the library: http://librarymanager/All#SparkFun_CCS811
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
#define CCS811_ADDR 0x5B //Default I2C Address
#define buffer 50

CCS811 ccs(CCS811_ADDR);
DHT dht(DHTPIN, DHTTYPE);

int index = 0;
float last[buffer];

void setup()
{
  Serial.begin(9600);
  dht.begin(); // initialize DHT22
  Wire.begin(); // initialize CCS811

  if (ccs.begin() == false)
  {
    Serial.print("CCS811 error");
    while (1)
      ;
  }
}

void loop()
{
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
      Serial.print(humi);
      Serial.print(",");
      Serial.print(avg(last));
      Serial.print(",");
      Serial.print(temp);
      Serial.print("");
  
      if (humi + 2 <= avg(last)) {
        Serial.print(",1");
      } else {
        Serial.print(",0");
      }
      
      if (ccs.dataAvailable()) {
        // read ccs data
        ccs.readAlgorithmResults();
        Serial.print(",");
        Serial.print(ccs.getCO2());
        Serial.print(",");
        Serial.print(ccs.getTVOC());
        Serial.println();
      }
    }
  }
  
  

  // wait a few seconds between measurements.
  if(index < buffer) {
    delay(1000);
  } else {
    delay(5000); 
  }
}

float avg(float arr[]) {
  float sum = 0;
  for (int i = 0; i < buffer; i++) {
    sum += arr[i];
  }
  return sum/buffer;
}
