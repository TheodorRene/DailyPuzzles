#!/usr/bin/python3

import sqlite3
from sys import argv
import subprocess


def converting(fen):
    cmd = 'curl http://www.fen-to-image.com/image/36/single/' + fen + ' | cat > position.png'
    subprocess.Popen(cmd,shell=True)

def main():
    fen,player = query()
    converting(fen)

def query():
    conn = sqlite3.connect('mateIn4.db')
    c = conn.cursor()

    getCount = "SELECT number FROM count"
    count = c.execute(getCount).fetchone()
    newCount = count[0] + 1
    num = count[0]

    updateCount = f"UPDATE count SET number={newCount}"
    getFen = f"SELECT fen FROM puzzle WHERE id={num}"
    getPlayer = f"SELECT to_move WHERE id={num}"
    c.execute(updateCount)
    fen = c.execute(getFen).fetchone()
    conn.commit()
    conn.close()
    return fen[0],getPlayer[0]

main()





