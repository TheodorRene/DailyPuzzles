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
