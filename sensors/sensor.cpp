//Generic Sensor Class
//Author: Kevin Murphy
//Date  : 15 - Oct - 14

#include "sensor.h"
#include <sys/time.h>
#include <wiringPi.h>
#include <iostream>
#include "mcp3008.h"
#include <string>

//Define the MCP3008 Pins -- WiringPi
//#define CLOCK   9 //Pi Pin 5
//#define SDA_CS  8 //Pi Pin 3
//#define ADC_IN  3 //Pi Pin 15
//#define ADC_OUT 2 //Pi Pin 13

#define CLOCK   11
#define SDA_CS  12
#define ADC_IN  15
#define ADC_OUT 13

//General Definitions
#define DEBUG 1

using namespace std;

Sensor::Sensor(string sensorName, int adcChannelNumber)
{
    name         = sensorName;
    adcChannelNo = adcChannelNumber;
};

Sensor::~Sensor(){}

//Code for reading values from MCP3008 ADC Chip
int Sensor::getADCResult(int adcChannelNo)
{
    if(DEBUG)
    {
	cout << "Calling getADCResult on Channel:: " << adcChannelNo << "\n";
    }
    return mcp3008_value(adcChannelNo, CLOCK, ADC_IN, ADC_OUT, SDA_CS );
}

string Sensor::getName()
{
    return name;
}

void Sensor::printName()
{
    cout << "Sensor : " << name << "\n";
}

int Sensor::getADCChannelNo()
{
    return adcChannelNo;
}

