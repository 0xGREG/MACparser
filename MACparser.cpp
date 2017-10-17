#include <iostream>
#include <list>
#include <string>
using namespace std;

list<string> findMACs(string text)
{
    list<string> macs;
    string currentMac = "";
    for (int i = 0; i < text.length(); i++)
    {
        bool correct = false;
        int position = currentMac.length() % 3;
        if (currentMac.length() < 17) {
            if (position < 2) {
                string characterSet = "0123456789ABCDEFabcdef";
                correct = (characterSet.find(text[i]) != string::npos);
            }
            else {
                correct = (text[i] == ':' || text[i] == '-');
            }
        }
        else if (text.length() < 20) {
            if (position == 2) {
                correct = (text[i] == '/');
            }
            else {
                string characterSet = "0123456789";
                correct = (characterSet.find(text[i] != string::npos));
            }
        }
        if (correct) {
            currentMac += text[i];
            if (currentMac.length() == 20) {
                macs.push_back(currentMac);
                currentMac = "";
            }
        }
        else {
            if (currentMac.length() > 2) {
                macs.push_back(currentMac);
            }
            currentMac = "";
            i--;
            continue;
        }
    }
    return macs;
}

void printList(list<string> text)
{
    for (list<string>::iterator it = text.begin(); it != text.end(); it++)
    {
        cout << *it << ", ";
    }
}

int main()
{
    printList(findMACs("00:11:2345:67:22:33:44:55:00:11:22:33:44:55/24:00:"));
    return 0;
}