/*
 * Data will come out on serial monitor in following format
 * humidity, avg. humidity, temperature, isWindowOpen(0/1), CO2, tVOC
 */

#include <Wire.h>
#include "SparkFunCCS811.h" //Click here to get the library: http://librarymanager/All#SparkFun_CCS811
#include "DHT.h"
#define DHTPIN 2
#define BUTTONPIN 4
#define LEDPIN 6
#define DHTTYPE DHT22
#define CCS811_ADDR 0x5B //Default I2C Address

//settings for z-score algorithm
#define lag 50
#define threshold 4
#define influence 0.5

CCS811 ccs(CCS811_ADDR);
DHT dht(DHTPIN, DHTTYPE);

int index = 0;
int reads = 0;
float y_rhum[lag];
float filteredY_rhum[lag];
float avgFilter[lag];
float getStdFilter[lag];
bool filterInit = false;

bool isWindowOpen = false;
int buttonState = 0;

void setup()
{
  pinMode(LEDPIN, OUTPUT);
  pinMode(BUTTONPIN, INPUT);
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
  buttonState = digitalRead(BUTTONPIN);

  if (buttonState == HIGH) {
    isWindowOpen = !isWindowOpen;
    if (isWindowOpen) {
      digitalWrite(LEDPIN, HIGH);
    } else {
      digitalWrite(LEDPIN,LOW);
    }
  }
  
  
  // read humidity
  float humi  = dht.readHumidity();
  float temp  = dht.readTemperature();
  
  // check if any reads failed
  if (isnan(humi)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    if (filterInit) {
      float rhum_mean = avg(y_rhum);
      Serial.print(humi);
      Serial.print(",");
      Serial.print(rhum_mean);
      Serial.print(",");
      Serial.print(temp);
      Serial.print(",");
  
      Serial.print(isWindowOpen);
      
      if (ccs.dataAvailable()) {
        // read ccs data
        ccs.readAlgorithmResults();
        Serial.print(",");
        Serial.print(ccs.getCO2());
        Serial.print(",");
        Serial.print(ccs.getTVOC());
      }
      Serial.println();
    }
    y_rhum[index] = humi;
    index = (index + 1) % 50;
    reads++;

    //initialize filter values for threshold algorithm
    if(index == lag - 1 && !filterInit) {
      avgFilter[0] = avg(y_rhum);
      getStdFilter[0] = getStd(y_rhum);
      filterInit = true;
    }
  }
  

  // wait a few seconds between measurements.
  if(reads < 2*lag) {
    delay(1000);
  } else {
    delay(5000); 
  }
}

float avg(float x[]) {
  float sum = 0;
  for (int i = 0; i < lag; i++) {
    sum += x[i];
  }
  return sum/lag;
}

float median(float x[], int xSize){
  
}

float getStd(float x[]) {
  float mean = avg(x);
  float sum = 0;
  float a, b;
  for (int i = 0; i < lag; i++) {
    a = abs(x[i] - mean);
    b = pow(a, 2);
    sum += b;
  }
  return sqrt(sum/lag);
}

int threshold_alg(float x) {
  int signal = 0;
  if (abs(x -  avgFilter[(index-1)%lag]) > threshold * getStdFilter[(index - 1)%lag]) {
    if (x > avgFilter[(index-1)%lag]) {
      signal = 1;
    } else {
      signal = -1;
    }
    filteredY_rhum[index] = influence*x + (1-influence)*filteredY_rhum[(index-1)%lag];
  } else {
    filteredY_rhum[index] = x;
  }
  avgFilter[index] = avg(filteredY_rhum);
  getStdFilter[index] = getStd(filteredY_rhum);
  return signal;
}
