# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:14:22 2016

@author: ericgrimson
"""

epsilon = 0.01
y = 135654.0
guess = y
numGuesses = 0

while abs(guess*guess - y) >= epsilon:
    numGuesses += 1
    guess = guess - (((guess**2) - y)/(2*guess))
    print('guess is: ' + str(guess))
print('numGuesses = ' + str(numGuesses))
print('Square root of ' + str(y) + ' is about ' + str(guess))
