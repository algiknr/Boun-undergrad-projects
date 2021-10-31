#include <iostream>
#include <string>
#ifndef PROJECT2_PASSENGER_H
#define PROJECT2_PASSENGER_H
using namespace std;


struct Passenger {
public:

int arrivaltime;
int luggagetime;
int flighttime;
int counterleavetime;
int securityleavetime;
int queuepriocriteria;
int securitytime;
string isluggage;
string isVIP;



    Passenger(float at, float pt, float lw, float sw, string v, string o);

};


#endif //PROJECT2_PASSENGER_H
