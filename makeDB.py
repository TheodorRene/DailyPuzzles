#!/usr/bin/python3

import sqlite3


def main():
    f = open('MateIn4.txt','r')
    l = makeList(f)
    f.close()


def reFormating(line):
    l = line.split(" ")
    return l[0],l[1]

def makeList(f):
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    c.execute("CREATE TABLE puzzle (id INTEGER PRIMARY KEY,fen text, to_move text)")
    l = []
    i = 1
    for line in f:
        if (i-2)%5 == 0:
            fen,color = reFormating(line)
            tup = (fen, color, lastLine)
            l.append(tup)
            dbReq = f"INSERT INTO puzzle (fen,to_move) VALUES ('{fen}','{color}')"
            c.execute(dbReq)
        lastLine = line.rstrip() # Players 
        i+=1
    conn.commit()
    conn.close()
    return l

main()
