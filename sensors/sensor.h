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
        string name;
        int    adcChannelNo;

    public:
        Sensor(string name, int adcChannelNo);
        ~Sensor();

        virtual void  initPins()   = 0; //Pure Virtual
        virtual float readValues() = 0; //Pure Virtual   
        
        int getADCResult();
        string getName();
        void printName();
        int  getADCChannelNo();

}

#endif
