
#include "Passenger.h"
using namespace std;



Passenger::Passenger(float at, float pt, float lw, float sw, string v, string o) {
    this-> arrivaltime=at;
    this-> luggagetime=lw;
    this->flighttime=pt;
    this->counterleavetime=0;
    this->securityleavetime=0;
    this->queuepriocriteria=0;
    this->securitytime=sw;
    this-> isluggage=o;
    this->isVIP=v;



}
;
