#!/home/theodorc/dev/Python-3.6.5/python

import sqlite3
from sys import argv
from os import path

# \s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s* possible regex for verifing FEN

config = {
    "mod": 5,
    "offset": 1
}

""" Main function """
def main():
    if len(argv) > 1 and argv[1] == "-a":
        try:
            print("Adding " + argv[2] + " to the puzzle database")
            add(argv[2])
            print("Database has been updated")
        except:
            raise Exception("No argument given to add")
    elif argv[1] == '-t':
        print("testing parsing")
        parse_file(argv[2], True)
    elif argv[1] == '--help':
        print("-a FILE : parse FILE and add to database")
        print("-t FILE : parse FILE and show parsing for test purposes")
        print("FILE : parse FILE and make database file mateIn4.db if it doesnt exist")
    else:
        if path.exists("mateIn4.db"):
            raise Exception('Database file already exists')
        print("Making database from argument")
        makeList(argv[1])
        print("MateIn4.db has been made")


def parse_file(file, isTestRun):
    """ Parse file as according to config parameters """
    f = open(file, 'r')
    lines = f.read().splitlines()
    parsed_data = []
    lines_printed = 0
    for i in range(2, len(lines)-1):
        if (i-config['offset']) % config['mod'] == 0:
            solution = lines[i+1]
            fen, color = reFormating(lines[i])
            if isTestRun:
                if lines_printed < 10: # Allow user to go through the parsed line 10 at a time
                    print_debug_info(fen, color, solution)
                    lines_printed += 1
                else:
                    ans = input("Do you want to see 10 more lines?[Y,n]")
                    if ans in ['n', 'N', 'No']:
                        print("Finished")
                        return
                    print_debug_info(fen, color, solution)
                    lines_printed = 0

            else:
                parsed_data.append((fen, color, solution))
    f.close()
    return parsed_data


def print_debug_info(fen, color, solution):
    """ Print debug info """
    print("fen", fen)
    print("color", color)
    print("solution", solution)


def add(file):
    """ Add more puzzles to database. Remember formatting from matein4.txt """
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    parsed_data = parse_file(file, False)
    for data in parsed_data:
        fen, color, solution = data
        dbReq = f"INSERT INTO puzzle (fen,to_move,solution) VALUES ('{fen}','{color}','{solution}')"
        c.execute(dbReq)
    conn.commit()
    conn.close()

def reFormating(line):
    """" split line for proper parsing """
    l = line.split(" ")
    return l[0], l[1]

def makeList(file):
    """
    Creates puzzle table, adds parsed data from text file to the database, then
    creates count table
    """
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    #Make table
    c.execute("CREATE TABLE puzzle (id INTEGER PRIMARY KEY,fen text, to_move text,solution text)")
    conn.commit()
    c.close()
    add(file)
    #Reestablish connection
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()
    # make counting table
    c.execute("CREATE TABLE count (id INTEGER PRIMARY KEY, number INTEGER)")
    c.execute("INSERT INTO count (number) VALUES (1)")

    conn.commit()
    conn.close()

main()
