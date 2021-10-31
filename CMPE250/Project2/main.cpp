#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <iterator>
#include "Passenger.h"
#include <queue>
#include <algorithm>
#include <list>

using namespace std;

template <class Container>
void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss),
              istream_iterator<string>(),
              back_inserter(cont));
}

struct CustomCompare {
    bool operator()(const Passenger &a, const Passenger &b) {
        if(a.queuepriocriteria==b.queuepriocriteria){
            return a.arrivaltime>b.arrivaltime;
        }else {

            return a.queuepriocriteria > b.queuepriocriteria;
        }

    }
};

string case8(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty()))
    {
        for (int i = SecurityList.size() - 1; i >= 0; i--)
        {
            Passenger pass = SecurityList.at(i);
            if (pass.securityleavetime == currenttime)
            {
                SecurityList.erase(SecurityList.begin()+i);
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        for (int i = CounterList.size() - 1; i >= 0; i--)
        {
            Passenger pass = CounterList.at(i);
            if (pass.counterleavetime == currenttime)
            {
                pass.queuepriocriteria = pass.flighttime;
                if(pass.isVIP!="V") {

                    SecurityQueue.push(pass);
                }else{
                    Totaltime=Totaltime+currenttime-pass.arrivaltime;
                    if (currenttime > pass.flighttime) {
                        missedflights = missedflights + 1;
                    }
                }
                CounterList.erase(CounterList.begin()+i);
            }
        }
        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        if (currentpassenger.arrivaltime == currenttime)
        {
            currentpassenger.queuepriocriteria = currentpassenger.flighttime;
            if ( currentpassenger.isluggage=="N" && currentpassenger.isVIP=="V")
            {
                Totaltime = Totaltime + currenttime - currentpassenger.arrivaltime;
                if (currenttime > currentpassenger.flighttime)
                {
                    missedflights = missedflights + 1;

                }
            }
            else if(currentpassenger.isluggage=="N") {

                SecurityQueue.push(currentpassenger);
            }else{
                PassengerQueue.push(currentpassenger);
            }
            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;
}
string case7(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty())) {

        for (int i = SecurityList.size() - 1; i >= 0; i--) {

            Passenger pass=SecurityList.at(i);
            if (pass.securityleavetime == currenttime) {
                SecurityList.erase(SecurityList.begin()+i);
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        for (int i = CounterList.size() - 1; i >= 0; i--) {

            Passenger pass =CounterList.at(i);
            if (pass.counterleavetime == currenttime) {
                pass.queuepriocriteria = currenttime;
                if(pass.isVIP!="V") {

                    SecurityQueue.push(pass);
                }else{
                    Totaltime=Totaltime+currenttime-pass.arrivaltime;
                    if (currenttime > pass.flighttime) {
                        missedflights = missedflights + 1;
                    }
                }
                CounterList.erase(CounterList.begin()+i);
            }
        }

        if (currentpassenger.arrivaltime == currenttime) {
            currentpassenger.queuepriocriteria = currenttime;
            if ( currentpassenger.isluggage=="N" && currentpassenger.isVIP=="V")
            {
                Totaltime = Totaltime + currenttime - currentpassenger.arrivaltime;
                if (currenttime > currentpassenger.flighttime)
                {
                    missedflights = missedflights + 1;

                }
            }
             else if(currentpassenger.isluggage=="N") {

                SecurityQueue.push(currentpassenger);
            }else{
                PassengerQueue.push(currentpassenger);
            }

            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT) {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();

            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while (SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT) {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;


}
string case6(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty()))
    {
        for (int i = SecurityList.size() - 1; i >= 0; i--)
        {
            Passenger pass = SecurityList.at(i);
            if (pass.securityleavetime == currenttime)
            {
                SecurityList.erase(SecurityList.begin()+i);
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        for (int i = CounterList.size() - 1; i >= 0; i--)
        {
            Passenger pass = CounterList.at(i);
            if (pass.counterleavetime == currenttime)
            {
                pass.queuepriocriteria = pass.flighttime;
                SecurityQueue.push(pass);
                CounterList.erase(CounterList.begin()+i);
            }
        }
        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        if (currentpassenger.arrivaltime == currenttime)
        {
            currentpassenger.queuepriocriteria = currentpassenger.flighttime;
            if(currentpassenger.isluggage=="N") {

                SecurityQueue.push(currentpassenger);
            }else{
                PassengerQueue.push(currentpassenger);
            }
            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;

}
string case4(int P,int L,int S,vector<Passenger>passengerlist) {
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty()))
    {
        for (int i = SecurityList.size() - 1; i >= 0; i--)
        {
            Passenger pass = SecurityList.at(i);
            if (pass.securityleavetime == currenttime)
            {
                SecurityList.erase(SecurityList.begin()+i);
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        for (int i = CounterList.size() - 1; i >= 0; i--)
        {
            Passenger pass = CounterList.at(i);
            if (pass.counterleavetime == currenttime)
            {
                pass.queuepriocriteria = pass.flighttime;
                if(pass.isVIP!="V") {

                    SecurityQueue.push(pass);
                }else{
                    Totaltime=Totaltime+currenttime-pass.arrivaltime;
                    if (currenttime > pass.flighttime) {
                        missedflights = missedflights + 1;
                    }
                }

                CounterList.erase(CounterList.begin()+i);
            }
        }
        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        if (currentpassenger.arrivaltime == currenttime)
        {
            currentpassenger.queuepriocriteria = currentpassenger.flighttime;
            PassengerQueue.push(currentpassenger);
            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;

}
string case3(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty())) {
        for (int i = SecurityList.size() - 1; i >= 0; i--) {

            Passenger pass=SecurityList.at(i);
            if (pass.securityleavetime == currenttime) {
                SecurityList.erase(SecurityList.begin()+i);
                
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        for (int i = CounterList.size() - 1; i >= 0; i--) {

            Passenger pass =CounterList.at(i);
            if (pass.counterleavetime == currenttime) {
                pass.queuepriocriteria = currenttime;
                if(pass.isVIP!="V") {

                    SecurityQueue.push(pass);
                }else{
                    Totaltime=Totaltime+currenttime-pass.arrivaltime;
                    if (currenttime > pass.flighttime) {
                        missedflights = missedflights + 1;
                    }
                }
                CounterList.erase(CounterList.begin()+i);
            }
        }

        if (currentpassenger.arrivaltime == currenttime) {
            currentpassenger.queuepriocriteria = currenttime;
            PassengerQueue.push(currentpassenger);

            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT) {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();

            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while (SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT) {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;

}
string case2(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty()))
    {
        for (int i = SecurityList.size() - 1; i >= 0; i--)
        {
            Passenger pass = SecurityList.at(i);
            if (pass.securityleavetime == currenttime)
            {
                SecurityList.erase(SecurityList.begin()+i);
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        for (int i = CounterList.size() - 1; i >= 0; i--)
        {
            Passenger pass = CounterList.at(i);
            if (pass.counterleavetime == currenttime)
            {
                pass.queuepriocriteria = pass.flighttime;
                SecurityQueue.push(pass);
                CounterList.erase(CounterList.begin()+i);
            }
        }
        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        if (currentpassenger.arrivaltime == currenttime)
        {
            currentpassenger.queuepriocriteria = currentpassenger.flighttime;
            PassengerQueue.push(currentpassenger);
            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT)
        {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();
            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT)
        {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;
}
string case5(int P,int L,int S,vector<Passenger>passengerlist){
    int currenttime = 0;
    int missedflights = 0;
    float Totaltime = 0.00F;
    Passenger currentpassenger = passengerlist.front();
    float avgtime;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
    vector<Passenger> CounterList;
    priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
    vector<Passenger> SecurityList;
    int COUNTERCOUNT = L;
    int SECURITYCOUNT = S;
    int PASSENGERCOUNT = P;

    while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty())) {
        for (int i = SecurityList.size() - 1; i >= 0; i--) {

            Passenger pass=SecurityList.at(i);
            if (pass.securityleavetime == currenttime) {
                SecurityList.erase(SecurityList.begin()+i);
                
                Totaltime = Totaltime + currenttime - pass.arrivaltime;
                if (currenttime > pass.flighttime)
                    missedflights = missedflights + 1;
            }
        }
        for (int i = CounterList.size() - 1; i >= 0; i--) {

            Passenger pass =CounterList.at(i);
            if (pass.counterleavetime == currenttime) {
                pass.queuepriocriteria = currenttime;
                SecurityQueue.push(pass);
                CounterList.erase(CounterList.begin()+i);
            }
        }

        if (currentpassenger.arrivaltime == currenttime) {
            currentpassenger.queuepriocriteria = currenttime;
            if(currentpassenger.isluggage=="N") {

                SecurityQueue.push(currentpassenger);
            }else{
                PassengerQueue.push(currentpassenger);
            }

            passengerlist.erase(passengerlist.begin());
            if (passengerlist.size() > 0)
                currentpassenger = passengerlist.front();
        }


        while(PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT) {
            Passenger passenger = PassengerQueue.top();
            PassengerQueue.pop();

            passenger.counterleavetime = currenttime + passenger.luggagetime;
            CounterList.push_back(passenger);

        }
        while(SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT) {
            Passenger passenger = SecurityQueue.top();
            SecurityQueue.pop();
            passenger.securityleavetime = currenttime + passenger.securitytime;
            SecurityList.push_back(passenger);
        }
        currenttime++;
    }
    avgtime = Totaltime / PASSENGERCOUNT;
    string a=to_string(avgtime)+" "+to_string(missedflights);
    return a;


}

    string case1(int P, int L, int S, vector<Passenger> passengerlist) {
        int currenttime = 0;
        int missedflights = 0;
        float Totaltime = 0.00F;
        Passenger currentpassenger = passengerlist.front();
        float avgtime;
        priority_queue<Passenger, vector<Passenger>, CustomCompare> PassengerQueue;
        vector<Passenger> CounterList;
        priority_queue<Passenger, vector<Passenger>, CustomCompare> SecurityQueue;
        vector<Passenger> SecurityList;
        int COUNTERCOUNT = L;
        int SECURITYCOUNT = S;
        int PASSENGERCOUNT = P;

        while (!(passengerlist.empty()&&PassengerQueue.empty()&&CounterList.empty()&&SecurityQueue.empty()&&SecurityList.empty())) {

            for (int i = SecurityList.size() - 1; i >= 0; i--) {

                Passenger pass=SecurityList.at(i);
                if (pass.securityleavetime == currenttime) {
                 SecurityList.erase(SecurityList.begin()+i);

                    
                    Totaltime = Totaltime + currenttime - pass.arrivaltime;
                    if (currenttime > pass.flighttime)
                        missedflights = missedflights + 1;
                }
            }
            for (int i = CounterList.size() - 1; i >= 0; i--) {

                Passenger pass =CounterList.at(i);
                if (pass.counterleavetime == currenttime) {
                    pass.queuepriocriteria = currenttime;
                    SecurityQueue.push(pass);
                    CounterList.erase(CounterList.begin()+i);
                }
            }

            if (currentpassenger.arrivaltime == currenttime) {
                currentpassenger.queuepriocriteria = currenttime;
                PassengerQueue.push(currentpassenger);

                passengerlist.erase(passengerlist.begin());
                if (passengerlist.size() > 0)
                    currentpassenger = passengerlist.front();
            }


            while (PassengerQueue.size() > 0 && CounterList.size() < COUNTERCOUNT) {
                Passenger passenger = PassengerQueue.top();
                PassengerQueue.pop();

                passenger.counterleavetime = currenttime + passenger.luggagetime;
                CounterList.push_back(passenger);

            }
            while (SecurityQueue.size() > 0 && SecurityList.size() < SECURITYCOUNT) {
                Passenger passenger = SecurityQueue.top();
                SecurityQueue.pop();
                passenger.securityleavetime = currenttime + passenger.securitytime;
                SecurityList.push_back(passenger);
            }

           currenttime++;
        }
        avgtime = Totaltime / PASSENGERCOUNT;

        string a=to_string(avgtime)+" "+to_string(missedflights);
        return a;



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
        int PASSENGERCOUNT = stoi(words[0]);
        int COUNTERCOUNT = stoi(words[1]);
        int SECURITYCOUNT = stoi(words[2]);


        vector<Passenger> PassengerList;
        
        vector<string> word;
        
        for (int i = 0; i < PASSENGERCOUNT; i++) {
            getline(infile, line);
            split1(line, word);
            float arrivaltime = stoi(word[0]);

            float flighttime = stoi(word[1]);
            float luggagewait = stoi(word[2]);
            float securitywait = stoi(word[3]);

            string vip = word[4];
            string onlinet = word[5];



            PassengerList.push_back(Passenger(arrivaltime, flighttime, luggagewait, securitywait, vip, onlinet));
            word.clear();
        }

        string a=case1(PASSENGERCOUNT, COUNTERCOUNT, SECURITYCOUNT, PassengerList);
        string b=case2(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string c= case3(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string d=case4(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string e=case5(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string f=case6(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string g=case7(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);
        string h=case8(PASSENGERCOUNT,COUNTERCOUNT,SECURITYCOUNT,PassengerList);

        ofstream myfile;
        myfile.open (argv[2]);
        myfile<<a<<endl;
        myfile<<b<<endl;
        myfile<<c<<endl;
        myfile<<d<<endl;
        myfile<<e<<endl;
        myfile<<f<<endl;
        myfile<<g<<endl;
        myfile<<h<<endl;
        myfile.close();

        cout << "input file has been read" << endl;






        return 0;
    }





