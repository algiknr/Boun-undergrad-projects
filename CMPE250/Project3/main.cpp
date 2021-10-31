#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <iterator>
#include <queue>
#include <stack>
#include "Node.h"
#include "algorithm"
#include "set"

using namespace std;

template <class Container>

void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss),
         istream_iterator<string>(),
         back_inserter(cont));
}
set<int>badsccno;

vector<int>last(vector<Node>&nodelist,vector<vector<int>> &sccnodearrays,int nodenumbers){
    for(int i=0;i<nodenumbers;i++){
        for (int k = 0; k < nodelist[i].numberoflinks; k++) {
            if (nodelist[i].sccno != nodelist[nodelist[i].links[k] - 1].sccno) {

                badsccno.insert(nodelist[nodelist[i].links[k] - 1].sccno);
            }
        }

    }

    vector<int>check;
    vector<int>a;
    int count=0;
    for (const int &number : badsccno) {
        while(count!=number){
                check=sccnodearrays[count];
                a.push_back(check[0]);
            count++;
        }
        count++;

    }
    if(count+1<=sccnodearrays.size()){
        for(int i=count;i<sccnodearrays.size();i++ ){
            check=sccnodearrays[i];
            a.push_back(check[0]);

        }
    }

    return a;
}



vector<Node>nodelist;
vector<vector<int>> sccnodearrays;
stack<int> S;
int nodenumbers;
int index=0;
int sccno=0;
void strongconnect(Node &v) {
    v.index = index;
    v.lowlink = index;
    index = index + 1;
    S.push(v.nodenumber);
    v.undefined = false;
    v.onstack = true;
    for (int j = 0; j < v.numberoflinks; j++) {
        if (nodelist.at(v.links.at(j) - 1).undefined) {
            strongconnect(nodelist.at(v.links.at(j) - 1));
            v.lowlink = min(v.lowlink, nodelist.at(v.links.at(j) - 1).lowlink);
        } else if (nodelist.at(v.links.at(j) - 1).onstack) {
            v.lowlink = min(v.lowlink, nodelist.at(v.links.at(j) - 1).index);
        }
    }


    int w=0;
    if (v.lowlink == v.index) {
        vector<int>sccnodes;

        do{

            w = S.top();
            nodelist[S.top()- 1].sccno = sccno;
            nodelist[S.top()-1].onstack = false;

            S.pop();
            sccnodes.push_back(w);


        }while (w != v.nodenumber);


        sccnodearrays.push_back(sccnodes);

        sccno++;

    }

}




vector<int> trojan(int nodenumbers2,vector<Node>&nodelist2) {
    nodelist=nodelist2;
    nodenumbers=nodenumbers2;
    for (int i = 0; i < nodenumbers; i++) {
        if (nodelist.at(i).undefined) {

            strongconnect(nodelist.at(i));


        }
    }



  return last(nodelist,sccnodearrays,nodenumbers);
}



int main(int argc, char *argv[]) {
    // below reads the input file
    // in your next projects, you will implement that part as well
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;



    // here, perform the input operation. in other words,
    // read the file named <argv[1]>
    ifstream infile(argv[1]);
    string line;
    // process first line
    getline(infile, line);
    vector<string> words;
    split1(line, words);
    int NODECOUNT = stoi(words[0]);


    vector<Node> nodelist;
    vector<string> word;
    vector<int>links;
    for (int i = 0; i < NODECOUNT; i++) {

        getline(infile, line);
        split1(line, word);
        int nodenumber =i+1;
        int numberoflinks=stoi(word[0]);

        for(int j=1;j<=numberoflinks;j++) {

            links.push_back(stoi(word[j]));
        }

        nodelist.push_back(Node(nodenumber, numberoflinks, links));
        links.clear();
        word.clear();
    }
    vector<int>finale;

    finale= trojan(NODECOUNT,nodelist);
    ofstream myfile;
    myfile.open (argv[2]);
    myfile<<finale.size()<<" ";
    for(int i=0; i<finale.size();i++) {
        myfile << finale[i]<< " ";
    }

    myfile.close();

    return 0;


}
