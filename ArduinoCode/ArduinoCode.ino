// Demo code for Grove - Temperature Sensor V1.1/1.2
// Loovee @ 2015-8-26

#include <math.h>

const int B = 4275;               // B value of the thermistor
const int R0 = 100000;            // R0 = 100k
const int pinTempSensor = A0;     // Grove - Temperature Sensor connect to A0

const int pinSoilSensor = A1;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int a = analogRead(pinTempSensor);

  float R = 1023.0 / a - 1.0;
  R = R0 * R;

  float temperature = 1.0 / (log(R / R0) / B + 1 / 298.15) - 273.15; // convert to temperature via datasheet

  Serial.print("temperature = ");
  Serial.println(temperature);

  Serial.print("Soil Moisture = ");
  //get soil moisture value from the function below and print it
  Serial.println(analogRead(pinSoilSensor));

  delay(1000);
}
