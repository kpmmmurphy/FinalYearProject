//Example Sensor Implementation
//Author: Kevin Murphy
//Date  : 15 - Oct - 14

#include <stdio.h>
#include <sys/time.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <iostream>
//#include <string>
#include "sensor.h"

using namespace std;

//Sensor Pin Definitions

//General Definitions
#define DEBUG 1
#define NAME "Thermistor"
#define ADC_CHANNEL_NO 0

class Thermistor : public Sensor
{
    public:
        Thermistor(string name, int adcChannelNo) : Sensor(name, adcChannelNo){}

	void initPins()
	{
	    if(wiringPiSetup() == -1)
	    {
	        printf("Setup WiringPi Failed!\n");
		exit(1);
	    }

	    //Pin Modes here

	    if(DEBUG)
   	    {
	        cout << "Setup : " << Sensor::getName() << "\n";
	    }
	}

	int readValue()
	{
	    if(DEBUG)
	    {
	        cout << "Reading Value of : " << Sensor::getName() << "\n";
	    }

	    int result = Sensor::getADCResult(Sensor::getADCChannelNo()); 
            printf("Result %d\n", result);

            return result;
	}
};

//Extern for Ctypes in Python
extern "C"
{
    Thermistor *Thermistor_new(char *name, int adcChannelNo){return new Thermistor(name, adcChannelNo);}
    void  Thermistor_initPins(Thermistor *sensor){sensor->initPins();}
    int   Thermistor_readValue(Thermistor *sensor){return sensor->readValue();}
    int   test(){return 1;}
}

int main(int argc, const char* argv[])
{
    Thermistor thermistor(NAME, ADC_CHANNEL_NO);
    //thermistor.initPins();
    thermistor.readValue();
    cout << "Done";
    return 0;
}
