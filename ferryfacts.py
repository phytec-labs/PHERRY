from random import *
import time

#Old Code from when we thought we could do loops on QT, made it not repeat itself
'''
#Runs forever
while True:
#variables
    alreadysaid = []

#Read facts
    with open('ferryfacts.txt', 'r') as f:
        lines = f.read().splitlines()
        numf = len(lines)

#Randomize facts, say fact, sleep, say new fact
    for x in range(0, numf):
        randF = randint(0, numf-1)
        while randF in alreadysaid:
            randF = randint(0, numf-1)
        alreadysaid.append(randF)
        print(lines[randF])
        time.sleep(60)

#Reads and parses file
with open('ferryfacts.txt', 'r', encoding="utf-8") as g:
    lines = g.read().splitlines()
with open("alreadyasked.txt", encoding="utf-8") as f:
    line = f.read().splitlines()
#Counts number of lines    
llines = len(lines)
lline = len(line)

#if amount of lines in ferry facts is = amount of lines in alreadyasked, clear alreadyasked
if len(lines) == len(line):
    with open('alreadyasked.txt', 'w', encoding="utf-8") as k:
        k.write("")

#random question, makes it not repeat
randF = randint(0, llines-1)
while str(randF) in line:
    randF = randint(0, llines-1)
print(lines[randF])

#add question to alreadyasked file so not repeated
with open('alreadyasked.txt', 'a', encoding="utf-8") as h:
    h.write(str(randF) + "\n")'''

with open('ferryfacts.txt', 'r', encoding="utf-8") as g:
    lines = g.read().splitlines()
llines = len(lines)
randF = randint(0, llines-1)
print(lines[randF])