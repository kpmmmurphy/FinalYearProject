//Generic Sensor Class
//Author: Kevin Murphy
//Date  : 15 - Oct - 14

#include "sensor.h"
#include <sys/time.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <iostream>
#include "mcp3004.h"
#include <string>
#include <unistd.h>

//Define the MCP3008 Pins -- WiringPi
//#define CLOCK   11 //Pi Pin 5
//#define SDA_CS  12 //Pi Pin 3
//#define ADC_IN  15 //Pi Pin 15
//#define ADC_OUT 13 //Pi Pin 13

//BCM Mode
//#define CLOCK   17
//#define SDA_CS  18
//#define ADC_IN  22
//#define ADC_OUT 27

//Define MCP3008 Fields-- WiringPi 
#define SPI_CHAN 0

//General Definitions
#define DEBUG 1

using namespace std;

Sensor::Sensor(string sensorName, int adcChannelNumber)
{
    name         = sensorName;
    adcChannelNo = adcChannelNumber;

    if(wiringPiSetup() < 0)
    {
        cout << "WiringPi Setup Failed...";
        exit(EXIT_FAILURE);
    }
    
    if(adcChannelNumber)
    {
        mcp3004Setup(100, SPI_CHAN);
    }
};

Sensor::~Sensor(){}

//Code for reading values from MCP3008 ADC Chip
int Sensor::getADCResult(int adcChannelNo)
{
    int BASE = 100; //MCP3008 channels are 100 - 107
    int result = analogRead(BASE + adcChannelNo);

    if(DEBUG)
    {
	cout << getName() << " -> Analog Result :: " << result << "\n";
    }

    return result;
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

