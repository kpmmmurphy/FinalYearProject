//MQ2 Carbon Dioxide Sensor Implementation
//Author: Kevin Murphy
//Date  : 15 - Oct - 14

#include <stdio.h>
#include <sys/time.h>
#include <wiringPi.h>
#include <stdlib.h>
#include <iostream>
#include <cmath>
#include "sensor.h"

using namespace std;

//General Definitions
#define DEBUG 1
#define NAME "MQ2 Flammable Gas"
#define ADC_CHANNEL_NO 2

class MQ2 : public Sensor
{
    public:
        MQ2(char *name, int adcChannelNo) : Sensor(name, adcChannelNo){}

	void initPins()
	{
	    if(DEBUG)
   	    {
	        cout << "Setup : " << Sensor::getName() << "\n";
	    }
	}

	int readValue()
	{	 
	    int result = Sensor::getADCResult(Sensor::getADCChannelNo()); 
	    if(DEBUG)
	    {
	        cout << Sensor::getName() << " -> Result :: "<< result << "\n";
	    }
        return result;
	}
};

//Extern for Ctypes in Python
extern "C"
{
    MQ2* MQ2_newInstance(char *name, int adcChannelNo)
    {
        return new MQ2(name, adcChannelNo);
    }
    void  MQ2_initPins(MQ2 *sensor){sensor->initPins();}
    int   MQ2_readValue(MQ2 *sensor){return sensor->readValue();}
    int   MQ2_test(){return -1;}
}

/*
int main(int argc, const char* argv[])
{
    MQ7 mq7(NAME, ADC_CHANNEL_NO);
    mq7.initPins();
    while(1){
        mq7.readValue();
	sleep(6);
    }
    return 0;
}
*/
