#include "SurveyClass.h"
using namespace std;

SurveyClass::SurveyClass() {
    this->members= new LinkedList();
}

SurveyClass::SurveyClass(const SurveyClass &other) {

    if(other.members){
        this->members=new LinkedList(*(other.members));
    }
}

SurveyClass& SurveyClass::operator=(const SurveyClass &list) {

    if(list.members){
        delete this->members;
        this->members=new LinkedList(*(list.members));
    }

    return *this;
}

SurveyClass::SurveyClass(SurveyClass &&other) {

    this->members=move(other.members);
    if(other.members){
        this->members=new LinkedList(*(other.members));
    }

    other.members= nullptr;
}

SurveyClass& SurveyClass::operator=(SurveyClass &&list) {

    this->members=move(list.members);
    if(list.members){
        delete this->members;
        this->members=new LinkedList(*(list.members));
    }

    list.members= nullptr;
    return *this;
}

void SurveyClass::handleNewRecord(string _name, float _amount) {
    Node *temp= members->head;

if(members->head== nullptr){

    members->pushTail(_name,_amount);
}else {

    for(int i=0; i<members->length;i++){

        if (temp->name == _name) {

            members->updateNode(_name, _amount);
            return;

       }

        temp = temp->next;
    }
    members->pushTail(_name, _amount);

}

    }

    float SurveyClass::calculateMinimumExpense() {
        Node *temp = members->head;
        float min=members->head->amount;


        while (temp->next != nullptr) {
            if(temp->amount<min) {
                min=temp->amount;
            }
            temp = temp->next;
        }
        return min;
    }

    float SurveyClass::calculateMaximumExpense()  {

        Node *temp = members->head;
        float max=members->head->amount;
        while (temp->next != nullptr) {
        if(temp->amount>max) {
            max=temp->amount;
        }
        temp = temp->next;
    }
    return max;
}

float SurveyClass::calculateAverageExpense() {
    Node *temp= members->head;
    float total=0;
    float count=0;
    int change1=0;
    float change2=0;

    while (temp != nullptr) {
        total+=temp->amount;
        temp = temp->next;
        count++;
    }

    change1=total/count*100;
    change2=float(change1)/100;


    return change2;
}

SurveyClass::~SurveyClass(){
        if(members)
            delete members;
        }

