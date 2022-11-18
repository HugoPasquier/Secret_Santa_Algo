from enum import Enum
from random import randint
from typing import TYPE_CHECKING
import os
import smtplib, ssl
from email.mime.text import MIMEText
from getpass import getpass
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

# List Initialisation
PersonList = []
CoupleList = []
MailMap = {}

# Select the file to open
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename) # Debug

# Parsing Data from file
file = open(filename, 'r')
lines = file.readlines()

# Parsing PersonList
isInPersonSection = False
for line in lines :
    if line == '---Person---\n':
        isInPersonSection = True
        continue
    if line == '\n' and isInPersonSection:
        break
    if isInPersonSection :
        Person = line.rsplit(' : ')
        if len(Person) != 2:
            print("Person count " + len(Person))
            print("Error in Person Section")
        PersonList.append(Person[0])
        MailMap[Person[0]] = Person[1]  # add the mail to the map

# Parsing CoupleList
isInCoupleSection = False
for line in lines :
    if line == '---Couple---\n':
        isInCoupleSection = True
        continue
    if line == '\n' and isInCoupleSection:
        break
    if isInCoupleSection :
        Couple = line.rsplit()
        if len(Couple) != 2:
            print("Person count " + len(Couple))
            print("Error in Couple Section")
        CoupleList.append((Couple[0], Couple[1]))

file.close()

def person_except(person, couples):
    # for each couple, if person is in the couple, return the other person
    for couple in couples:
        if person in couple:
            if person == couple[0]:
                return couple[1]
            else:
                return couple[0]
    return None


# Return True if there is a person in the list that is not 'person' or in 'person's couple
def does_compute(santaList, person, person_mate = None) :
    for p in santaList:
        if p != person and p != person_mate:
            return True
    return False

# Take a random person from the list and return it with the new list, the chosen person can't be 'person' or in 'person's couple
def draw_off(santaList, person, person_mate = None) :
    while True :
        personID = randint(0, len(santaList) - 1)
        if ((santaList[personID] != person_mate and santaList[personID] != person)) :
            gift_to = santaList[personID]
            santaList.remove(gift_to)
            return (santaList, gift_to)
            # not reached

def RunGiftList(persons, couples) :
    personToGiftList = []

    while(True) :
        santaList = persons.copy()
        giftMap = {}
        to_the_end = True

        while(to_the_end) :
            for elem in persons :
                if not does_compute(santaList, elem, person_except(elem, couples)) :
                    to_the_end = False
                    break
                new_list, person_to_gift = draw_off(santaList, elem, person_except(elem, couples))
                santaList = new_list
    
                giftMap[elem] = person_to_gift

                if len(giftMap) == len(persons) : 
                    return giftMap

        if(not to_the_end) :
            continue
    
        return giftMap


def printToFile(giftMap) :
    file_end_str = '_doit_offir_a.txt'
    data_dir = askdirectory()
    for elem in giftMap:
        file_str = data_dir + '/' + elem + '/' + elem + file_end_str
        if not os.path.exists(data_dir + '/' + elem) :
            os.makedirs(data_dir + '/' + elem)
        else :
            for file in os.listdir(data_dir + elem) :
                os.remove(data_dir + '/' + elem + '/' + file)

        file = open(file_str, "a")
        str_gift = "Personne à qui offrir : " + giftMap[elem]
        file.write(str_gift)
        file.close()


### No Longer Working due to the evolution of Google Policy in matter of non secure third part App ###
def emailSending(giftMap) :
    port = 465  # For SSL
    mail = input('Saisir l\'adresse mail : \n')

    print('Saisir le mot de passe associé au compte mail : ')
    password = getpass()

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        sender_email = mail
        
        # Sending emails
        for elem in giftMap :

            #receiver_email = MailMap(elem)
            receiver_email = MailMap(elem)
            message = MailMap(elem) + '''
            La personne à qui tu dois offrir un cadeau est ''' + giftMap(elem) + '''
            Personne d'autres que toi n'est au courant de qui tu t'occupes.
            
            PS : Ce mail a été envoyé de manière automatique, merci de ne pas y répondre.

            Bon achat de Noël !
            '''
            msg = MIMEText(message)
            msg['Subject'] = 'Tirage Père Noël Surprise'
            msg['From'] = mail
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())




result_map = RunGiftList(PersonList, CoupleList)
print(result_map)
printToFile(result_map)