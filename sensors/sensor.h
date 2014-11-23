//Sesnor.h
//Author: Kevin Murphy
//Date  : 16 - Oct - 14

#ifndef __SENSOR_H_INCLUDED__
#define __SENSOR_H_INCLUDED__

using namespace std;

#include <string>

class Sensor
{
    private:
        char  *name;
        int    adcChannelNo;

    public:
        Sensor(char *name, int adcChannelNo);
        ~Sensor();

        virtual void  initPins() = 0; //Pure Virtual
        virtual int readValue()  = 0; //Pure Virtual   
        
        int getADCResult(int adcChannelNo);
        char* getName();
        void printName();
        int  getADCChannelNo();
	static int spiSetup;

};

#endif
