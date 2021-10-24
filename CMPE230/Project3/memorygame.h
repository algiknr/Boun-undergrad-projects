#ifndef MEMORYGAME_H
#define MEMORYGAME_H

#include <QMainWindow>
#include <iostream>
#include <QTest>
#include <algorithm>
#include<ctime>
#include<cstdlib>

namespace Ui {
class memorygame;
}

class memorygame : public QMainWindow
{
    Q_OBJECT


public:
    explicit memorygame(QWidget *parent = nullptr);
    ~memorygame();

private:
    Ui::memorygame *ui;

private slots :
    void ButtonPressed();
    void ResetPressed();

};

#endif // MEMORYGAME_H
