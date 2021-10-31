#include "LinkedList.h"
using namespace std;
LinkedList::LinkedList() {
    this->length=0;
    this->head= nullptr;
    this->tail=nullptr;

}
LinkedList::LinkedList(const LinkedList& list) {
    this->length=list.length;


    if(list.head) {
        this->head = new Node(*(list.head));
    }

    Node*temp=this->head;
    while(temp->next!= nullptr){
        temp = temp->next;
    }
       this->tail= temp;


}

LinkedList& LinkedList::operator=(const LinkedList& list) {
    this->length=list.length;

    if(list.head) {
        delete this->head;
        this->head = new Node(*(list.head));
    }

        Node *temp = this->head;
       while(temp->next!= nullptr){
          temp = temp->next;
        }
        this->tail = temp;

    return *this;

}

LinkedList::LinkedList(LinkedList&& list) {
    this ->length=move(list.length);

    if(list.head) {
        this->head = new Node(*(list.head));
        this->tail=new Node(*(list.tail));
    }

    list.length = 0;
    list.head = nullptr;
    list.tail= nullptr;
}

LinkedList& LinkedList::operator=(LinkedList&& list) {
    this->length=move(list.length);

    if(list.head) {
        delete this->head;
        this->head = new Node(*(list.head));
        this->tail = new Node(*(list.tail));
    }

    list.length = 0;
    list.head = nullptr;
    list.tail= nullptr;

    return *this;
}

void LinkedList::pushTail(string _name, float _amount) {

        Node *final = new Node(_name,_amount);

        if (head == nullptr) {
            head =  final;
            tail=head;

            this->length++;
        } else {
            Node *temp = head;

                for(int i=0; i< length-1; i++) {
                    temp = temp->next;
                }

            tail=temp;
            tail->next=final;
            tail=final;

            this->length++;
        }


    }

void LinkedList::updateNode(string _name, float _amount) {

    Node *temp= head;
    
    for(int i=0; i<length; i++) {
        if (temp->name == _name) {
            temp->amount = _amount;
            
        }
        temp = temp->next;
    }
    }



LinkedList::~LinkedList() {
    if(head){
        delete head;
    }
}

