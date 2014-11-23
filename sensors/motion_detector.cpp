//Example Sensor Implementation
//Author: Kevin Murphy
//Date  : 19 - Nov - 14

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
#define NAME "Motion Detector"
#define ADC_CHANNEL_NO -1

//Pin Definitions
#define MOTION_D_INPUT_PIN 7 //Pi Pin 7 ~ BCM Pin 4

class MotionDetector : public Sensor
{
    public:
        MotionDetector(char *name, int adcChannelNo) : Sensor(name, adcChannelNo){}

	void initPins()
	{
	    if(DEBUG)
   	    {
	        cout << "Setup : " << Sensor::getName() << "\n";
	    }
	    
	    pinMode(MOTION_D_INPUT_PIN,INPUT);
	}

	int readValue()
	{	
	    int result = digitalRead(MOTION_D_INPUT_PIN); 
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
    MotionDetector *MotionDetector_new(char *name, int adcChannelNo){return new MotionDetector(name, adcChannelNo);}
    void  MotionDetector_initPins(MotionDetector *sensor){sensor->initPins();}
    int   MotionDetector_readValue(MotionDetector *sensor){return sensor->readValue();}
    int   MotionDetector_test(){return 1;}
}
/*
int main(int argc, const char* argv[])
{
    MotionDetector motionDetector(NAME, ADC_CHANNEL_NO);
    motionDetector.initPins();
    while(1){
	if(motionDetector.readValue())
        {
            cout << "Motion Detected!\n";
	    system("../scripts/take_camera_still.sh");
	}
	sleep(6);
    }
    return 0;
}
*/
