#include "Node.h"
using namespace std;



Node::Node(float nodenumber, float numberoflinks, vector<int>links) {
    this-> nodenumber=nodenumber;
    this-> numberoflinks=numberoflinks;
    this->links=links;
    this->index=0;
    this->lowlink=0;
    this->undefined=true;
    this->onstack=false;
    this->sccno=0;


}
;

