#!/home/theodorc/dev/Python-3.6.5/python

import sqlite3
from sys import argv
from os import path

# \s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s* possible regex for verifing FEN


def main():
    if len(argv)>1 and argv[1]=="-a":
        print("Adding " + argv[2] + " to the puzzle database")
        add(argv[2])
        print("Database has been updated")
    else:
        if(path.exists("mateIn4.db")):
            raise Exception('Database file already exists')
        print("Making database from MateIn4.txt")
        f = open('MateIn4.txt','r')
        makeList(f)
        f.close()
        print("MateIn4.db has been made")

#Add more puzzles to database. Remember formatting from matein4.txt
def add(file):
    f = open(file,'r')
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    lines = f.read().splitlines()
    for i in range(2,len(lines)-1):
        if (i-1)%5 == 0:
            solution = lines[i+1]
            fen,color = reFormating(lines[i])
            dbReq = f"INSERT INTO puzzle (fen,to_move,solution) VALUES ('{fen}','{color}','{solution}')"
            c.execute(dbReq)
    conn.commit()
    conn.close()

def reFormating(line):
    l = line.split(" ")
    return l[0],l[1]

#Parses the txtfile and adds entries to the database
def makeList(f):
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    #Make table
    c.execute("CREATE TABLE puzzle (id INTEGER PRIMARY KEY,fen text, to_move text,solution text)")
    lines = f.read().splitlines()
    for i in range(2,len(lines)-1):
        #the fen comes at lines where i-1%5 is equal to zero
        if (i-1)%5 == 0:
            solution = lines[i+1]
            fen,color = reFormating(lines[i])
            dbReq = f"INSERT INTO puzzle (fen,to_move,solution) VALUES ('{fen}','{color}','{solution}')"
            c.execute(dbReq)
    # make counting table
    c.execute("CREATE TABLE count (id INTEGER PRIMARY KEY, number INTEGER)")
    c.execute("INSERT INTO count (number) VALUES (1)")

    conn.commit()
    conn.close()

main()
