#include <iostream>
#include <string>
#include<vector>

#ifndef PROJECT3_NODE_H
#define PROJECT3_NODE_H
 using namespace std;

class Node {
public:

    int nodenumber;
    int numberoflinks;
    vector<int>links;
    int index;
    int lowlink;
    int sccno;
    bool undefined;
    bool onstack;



    Node(float nodenumber, float numberoflinks, vector<int>links);

};


#endif //PROJECT3_NODE_H
