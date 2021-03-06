//MQ7 Carbon Dioxide Sensor Implementation
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
#define DEBUG 0
#define NAME "MQ7 Carbon Monoxide"
#define ADC_CHANNEL_NO 1

class MQ7 : public Sensor
{
    public:
        MQ7(char *name, int adcChannelNo) : Sensor(name, adcChannelNo){}

	void initPins()
	{
	    if(DEBUG)
   	    {
	        cout << "Setup : " << Sensor::getName() << "\n";
	    }
	}

	int readValue()
	{	
        //int result = (int)carbonMonoxideLevel( Sensor::getADCResult( Sensor::getADCChannelNo() )); 
	    int result = Sensor::getADCResult( Sensor::getADCChannelNo()); 
	    if(DEBUG)
	    {
	        cout << Sensor::getName() << " -> Result :: "<< result << "\n";
	    }
        return result;
	}

    private:
	
	double carbonMonoxideLevel(int RawADC) 
    {
  	    double co_level;
	    int resistor = 0; //Usuall 10000 for 10k
  	    co_level = log((double)((10240000/RawADC) - resistor) / 10000);
        return co_level;
    }
};

//Extern for Ctypes in Python
extern "C"
{
    MQ7* MQ7_newInstance(char *name, int adcChannelNo)
    {
        return new MQ7(name, adcChannelNo);
    }
    void  MQ7_initPins(MQ7 *sensor){sensor->initPins();}
    int   MQ7_readValue(MQ7 *sensor){return sensor->readValue();}
    int   MQ7_test(){return -1;}
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
