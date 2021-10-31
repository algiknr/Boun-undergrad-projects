#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <iterator>
#include <queue>
#include<cmath>
#include <chrono>


using namespace std;
using namespace std::chrono;

template <class Container>

void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss),
         istream_iterator<string>(),
         back_inserter(cont));
}
const long int INF = 9999999999;

typedef pair<int, int> iPair;



int shortestPath(int *graph, int V, int src, int target, int noofcolumns)
{
    priority_queue< iPair, vector <iPair>, greater<iPair> > pq;

    vector<int> dist(V, INF);
    vector<bool> visited(V, false);

    pq.push(make_pair(0, src));
    dist[src] = 0;

    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();

        for (int i = 0; i < 4; i++) {
            int v = 0;
            int weight = INF;
            // Get vertex label and weight of current adjacent
            // of u.
            int column = u % noofcolumns;
            if (i == 0 && column != noofcolumns - 1) // right neighbour
            {
                v = u + 1;
                weight = abs(graph[u] - graph[v]);
            }
            if (i == 1 && column != 0) // left neighbour
            {
                v = u - 1;
                weight = abs(graph[u] - graph[v]);
            }
            if (i == 2 && u > noofcolumns - 1) // upper neighbour
            {
                v = u - noofcolumns;
                weight = abs(graph[u] - graph[v]);
            }
            if (i == 3 && u < V - noofcolumns) // lower neighbour
            {
                v = u + noofcolumns;
                weight = abs(graph[u] - graph[v]);
            }
            int f = fmax(dist[u], weight);
            if (dist[v] > f) {
                dist[v] = f;
                pq.push(make_pair(dist[v], v));

            }
        }
        if (u == target)
            break;
    }
    return dist[target] ;
}


int main(int argc, char *argv[]) {
    cout<<"hello"<<endl;
    if (argc != 3) {

        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    ifstream infile(argv[1]);
    string line;

    getline(infile, line);
    vector<string> word1;
    split1(line, word1);
    int noofrows= stoi(word1[0]);
    int noofcolumns=stoi(word1[1]);

    int verticescount;


    verticescount = noofrows * noofcolumns;


    string word;
    int rowindex = 0;
    int columnindex = 0;
    int vertex = 0;
    int *mynewfile = new int[verticescount];
    vector<iPair>* adj;
    adj = new vector<iPair>[verticescount];

    while (infile >> word)
    {
        int val = stoi(word);
        mynewfile[vertex] = val;

        vertex++;
        if (vertex == verticescount)
            break;

    }

    int noofqueries;
    vector<int>queriesin;
    vector<vector<int>> queries;
    bool querycount = true;
    while (infile >> word)
    {

        int val = stoi(word);
        if (querycount)
        {
            noofqueries = val;
            querycount = false;
        }
        else
        {
            queriesin.push_back(val);
        }
        if (queriesin.size() == 4)
        {

            queries.push_back(queriesin);
            queriesin.clear();
        }



    }



    int index1=noofcolumns*(queries[0][0]-1)+queries[0][1]-1;
    int index2=noofcolumns*(queries[0][2]-1)+queries[0][3]-1;

    int result=shortestPath(mynewfile, verticescount, index1, index2, noofcolumns);
    ofstream myfile;
    myfile.open (argv[2]);
    myfile<<result<<endl;
    myfile.close();


    return 0;
}
