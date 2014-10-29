//Example Sensor Implementation
//Author: Kevin Murphy
//Date  : 15 - Oct - 14

#include <stdio.h>
#include <sys/time.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include "sensor.h"

using namespace std;

//Sensor Pin Definitions
#define 
#define

//General Definitions
#define DEBUG 1
class ExampleSensor : public Sensor
{
    public:
        ExampleSensor(string name, int adcChannelNo) : Sensor(name, adcChannelNo){}

	void initPins()
	{
	    if(wiringPiSetup() == -1)
	    {
	        printf("Setup WiringPi Failed!\n")
		exit(1);
	    }

	    //Pin Modes here

	    if(DEBUG)
   	    {
	        cout << "Setup : " << getName();
	    }
	}

	float readValue()
	{
	    if(DEBUG)
	    {
	        cout << "Reading Value of : " << getName();
	    }
	}
};

//Extern for Ctypes in Python
extern "C"
{
    ExampleSensor *ExampleSensor_new(char *name, int adcChannelNo){return new ExampleSensor(name, adcChannelNo);}
    void  ExampleSensor_initPins(Sensor *exampleSensor){exampleSensor->initPins();}
    float ExampleSensor_readValue(Sensor *exampleSensor){exampleSensor->readValue();}
    int   test(){return 1;}
}

