# AES Encoder/decoder
#
#  The MIT License (MIT)
#
# Copyright (c) 2017 Florian Madar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import pyaes
import re

file = "encrypted.txt"


### Econding and decoding functions

def encode():
    details = raw_input("Please enter account info: ").lower()
    username = raw_input("Enter username that will be encoded: ")
    message = raw_input("Enter password that will be encoded: ")
    key = raw_input("Enter a 16 characters encryption key: ")
    try:
        aes = pyaes.AESModeOfOperationOFB(key)
        encoded_password = aes.encrypt(message)
        data = details + ":" + username + ":" + encoded_password
        write_report(data, file)
    except ValueError:
        print "ERROR: Key must have 16 characters"


def return_data(details):
    open_file = open(file, "r")
    data = open_file.read()
    line = re.findall(details + ".*", data)
    if len(line) != 0:
        str = "".join(line)
        array = str.split(":")
        password = array[2]
        username = array[1]
        return username, password
    else:
        print "ERROR: Account info for %s does not exists \n" % details


def write_report(data, file):
    with open(file, "a") as input_file:
        input_file.write(data + "\n")


def decode():
    details = raw_input("Please enter account info: ").lower()
    key = raw_input("Enter 16 bit encryption key: ")
    try:
        password = return_data(details)[1]
        username = return_data(details)[0]
    except IOError:
        print "ERROR: File does not exist or you don't have read permission"
    else:
        try:
            aes = pyaes.AESModeOfOperationOFB(key)
            decoded = aes.decrypt(password)
            print "Username for the %s account is %s with password: " % (details, username), decoded
        except ValueError:
            print "ERROR: Key must have 16 characters"


### List accounts

def list_accounts():
    try:
        open_file = open(file, "r")
        data = open_file.read().splitlines()
        print "###Acounts###"
        for i in data:
            str = "".join(i)
            array = str.split(":")
            username = array[0]
            print "Account name: ", username
    except IOError:
        print "ERROR: File does not exist or you don't have read permission"


### Search for account name

def search():
    details = raw_input("Please enter account info: ").lower()
    try:
        open_file = open(file, "r")
        data = open_file.read()
    except IOError:
        print "File does not exist or access is denied"
    else:
        line = re.findall(".*" + details + ".*", data)
        for i in line:
            str = "".join(i)
            array = str.split(":")
            account = array[0]
            username = array[1]
            print "Account name=%s and username=%s" % (account, username)


def menu():
    meniu = 1
    while meniu:
        print "### MENU ###"
        print "1. Encode message"
        print "2. Decode message"
        print "3. List accounts saved in database"
        print "4. Search"
        print "5. Exit"
        choose = raw_input("Enter a number corresponding: ")
        if choose == "1":
            encode()
            print "\n"
        elif choose == "2":
            decode()
            print "\n"
        elif choose == "3":
            list_accounts()
            print "\n"
        elif choose == "4":
            search()
            print "\n"
        elif choose == "5":
            return
        else:
            print "Invalid option"
            print "\n"


menu()
