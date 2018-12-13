#!/usr/bin/python3

import sqlite3
from sys import argv


def main():
    if argv[1]=="-a":
        add(argv[2])
    else:
        f = open('MateIn4.txt','r')
        l = makeList(f)
        f.close()

def add(file)
    f = open(file,'r')
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    l = []
    lines = f.read().splitlines()
    for i in range(2,len(lines)-1):
        if (i-1)%5 == 0:
            solution = lines[i+1]
            fen,color = reFormating(lines[i])
            tup = (fen,color,solution)
            l.append(tup)
            dbReq = f"INSERT INTO puzzle (fen,to_move,solution) VALUES ('{fen}','{color}','{solution}')"
            c.execute(dbReq)
    conn.commit()
    conn.close()

def reFormating(line):
    l = line.split(" ")
    return l[0],l[1]

def makeList(f):
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    c.execute("CREATE TABLE puzzle (id INTEGER PRIMARY KEY,fen text, to_move text,solution text)")
    l = []
    lines = f.read().splitlines()
    for i in range(2,len(lines)-1):
        if (i-1)%5 == 0:
            solution = lines[i+1]
            fen,color = reFormating(lines[i])
            tup = (fen,color,solution)
            l.append(tup)
            dbReq = f"INSERT INTO puzzle (fen,to_move,solution) VALUES ('{fen}','{color}','{solution}')"
            c.execute(dbReq)
    conn.commit()
    conn.close()
    return l

main()
