#include "memorygame.h"
#include "ui_memorygame.h"


// Holds the first clicked card
 QPushButton *prevbutton;
//Holds the first clicked card
 QPushButton *currentbutton;
//Counter is for to keep track of the card number (*It also prevents the 3rd card being opened before the previous 2 card processed)
 int counter=0;
//Number of successfull pair of cards
 int pairs=0;
//Number of both successfull and unsuccessful pair of cards
 int tries=0;
//The vector that keeps the value letters of front faces of cards(front face card vector)
 std::vector<QString> myvector={"A","A","B","B","C","C","D","D","E","E","F","F","G","G","H","H","I","I","J","J","K","K","L","L"};
//Specific name of buttons to identify them
 QString buttonname;
//The button array
 QPushButton *numButtons[24];

//The line is necessary for randomization
int myrandom(int i){return std::rand()%i;}

// Constructor
memorygame::memorygame(QWidget *parent) :


    // Call the QMainWindow constructor
    QMainWindow(parent),

    // Create the UI class and assign it to the ui member
    ui(new Ui::memorygame)

{
   //This part randomizes the front faces on cards
   std::srand(unsigned(std::time(0)));
   std::random_shuffle(myvector.begin(),myvector.end(),myrandom);

    // Setup the UI
    ui->setupUi(this);

    //Initializes the pairs and tries lines as 0 and give the adjacent lines their names
    ui->p1->setText(" Pairs : ");
    ui->t1->setText(" Tries : ");
    ui->Pairs->setText(QString::number(pairs, 10));
    ui->Tries->setText(QString::number(tries, 10));


    // Will hold references to all the number buttons
    // Cycle through locating the buttons
    //Match the buttons with certains functions via signals
    for(int i = 0; i < 24; ++i){
        QString butName = "b" + QString::number(i);

        // Get the buttons by name and add to array
        numButtons[i] =memorygame::findChild<QPushButton *>(butName);


        // When the button is released call buttonpressed()
        connect(numButtons[i], SIGNAL(released()), this,
                SLOT(ButtonPressed()));
    }

        //If the button is reset it will go to a different function
        QPushButton* reset = memorygame::findChild<QPushButton *> ("Reset");
        connect(reset,SIGNAL(released()), this,SLOT(ResetPressed()));
}

//Destructor
memorygame::~memorygame()
{
    delete ui;
}

//This function holds the main logic of cards except reset button
void memorygame::ButtonPressed(){
    // When the counter is 0 it will get the first card only and store it in prevbutton.
    //Then we will change the text with corralating index between button number and randomized front face card vector
    if(counter==0){
    prevbutton =(QPushButton *)sender();
    buttonname=(*prevbutton).objectName();
    int butnum=buttonname.split("b").last().toInt();
    (*prevbutton).setText(myvector[butnum]);
    counter=1;

    //Below will take the second card
    }else if(counter==1) {

        currentbutton =(QPushButton *)sender();

        //This line prevent the consequences of clicking the same button
        if(QString::compare(currentbutton->objectName(), prevbutton->objectName())==0){
            return;
        }
        buttonname=(*currentbutton).objectName();
        int butnum=buttonname.split("b").last().toInt();
        (*currentbutton).setText(myvector[butnum]);

        //while displaying two cards result counter=2 will impede the 3rd card being opened
         counter=2;
        if(QString::compare(currentbutton->text(),prevbutton->text())==0){
            //The wait give the necessary time to compare
            QTest::qWait(1000);
            //After finding the pairs number will rise and the cards will disappear from grid
            pairs=pairs+1;
            (*prevbutton).hide();
            (*currentbutton).hide();

        }
        else {
            QTest::qWait(1000);
            //If it is not a pair it will turn their faces down
            (*prevbutton).setText("X");
            (*currentbutton).setText("X");

        }
        //Tries number will rise in both circumstances
        tries=tries+1;

        //Display the both tries and pairs results
        ui->Pairs->setText(QString::number(pairs, 10));
        ui->Tries->setText(QString::number(tries, 10));
        counter=0;
    }



}

//Reset button logic
void memorygame::ResetPressed(){
    //randomizes the vector again
    std::srand(unsigned(std::time(0)));
    std::random_shuffle(myvector.begin(),myvector.end(),myrandom);
    //faces down all the cards
    for(int i = 0; i < 24; ++i){
        numButtons[i]->show();
        numButtons[i]->setText("X");
    }
    //Resets all the variables and texts to their initial values
    counter=0;
    pairs=0;
    tries=0;
    ui->Pairs->setText(QString::number(pairs, 10));
    ui->Tries->setText(QString::number(tries, 10));

}
