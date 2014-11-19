//Example Sensor Implementation
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

	    int result = (int)thermistorTemp( Sensor::getADCResult( Sensor::getADCChannelNo() )); 
            
	    if(DEBUG)
	    {
		printf("Result %d\n", result);
	    }

            return result;
	}

    private:
	
	double thermistorTemp(int RawADC) 
        {
  	    double Temp;
            // We divide by our thermistor's resistance at 25C, in this case 10k
  	    Temp = log((double)((10240000/RawADC) - 10000) / 10000);
  	    Temp = 1 / (0.003354016 + (0.0002569850 * Temp) + (0.000002620131 * Temp * Temp)+ (0.00000006383091 * Temp * Temp * Temp));
            Temp = Temp - 273.15; // Convert Kelvin to Celsius
            return Temp;
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
/*
int main(int argc, const char* argv[])
{
    Thermistor thermistor(NAME, ADC_CHANNEL_NO);
    thermistor.initPins();
    while(1){
        thermistor.readValue();
	sleep(6);
    }
    return 0;
}
*/
