#include <iostream>

#include <sstream>

#include <fstream>

#include <vector>

#include <iterator>

#include <queue>

#include<cmath>

#include <chrono>

#include <algorithm>

#include <map>

#include<cstring>

#include <unordered_set>

#include <unordered_map>



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



long result = 0;

const long MYBASE = 1000000007;

unordered_map<string, long> mwnos;



static long Wordbreakfunction(unordered_set<string> dict, string str, unordered_set<string> mw) {

    long count = 0;

    if (str.length() == 0) {

        mw.clear();

        return (count + 1)%MYBASE;

    }

    if (mw.find(str) != mw.end()) {

        return (count + 1)%MYBASE;

    }

    for (int i = 1; i <= str.length(); i++) {

        string beginning = str.substr(0, i);

        if (dict.find(beginning) != dict.end()) {

            mw.insert(beginning);

            string rest = str.substr(i);

            if (mwnos.find(rest) == mwnos.end())

                count = count%MYBASE + Wordbreakfunction(dict, rest, mw);

            else

                count = count%MYBASE+ mwnos.at(rest);

        }

    }

    count = count % MYBASE;

    if (count <0 )

    {
        int x;

    }

    if (mwnos.find(str) == mwnos.end())

    {
        mwnos.insert(make_pair(str, count));

    }

    return count;
}

static int WBDP(unordered_set<string> dict, string str)

{

    unordered_set<string> memo;



    return Wordbreakfunction(dict, str, memo);

}



int main(int argc, char *argv[]) {



    cout<<"hello"<<endl;
    if (argc != 3) {

        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    ifstream infile(argv[1]);
    string word;
    int count = 0;
    string key;
    int sizedict = 0;
    unordered_set<string> dict;
    while (infile >> word)
    {
        if (count == 0) {

            key = word;
        }
        if (count == 1) {

            sizedict = stoi(word);

        }

        if (count>1) {

            string a = word;

            dict.insert(a);
        }

        count++;
    }
    result = WBDP(dict, key);

    ofstream myfile;
    myfile.open (argv[2]);
    myfile<<result<<endl;
    myfile.close();


    return 0;

}
