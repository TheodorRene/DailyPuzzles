#!/home/theodorc/dev/Python-3.6.5/python

from time import sleep
import tweepy
import sqlite3
from sys import argv
import subprocess

ANSWER = ""


def converting(fen):
    cmd = 'curl http://www.fen-to-image.com/image/36/single/coords/' + fen + ' | cat > /home/theodorc/dev/DailyPuzzles/position.png'
    subprocess.Popen(cmd,shell=True)

def main():
    fen,player = query()
    converting(fen)
    sleep(2)
    tweet(player)

def tweet(player):
    c_k,c_s,a_k,a_s = getKeys()
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    image = '/home/theodorc/dev/DailyPuzzles/position.png'

    if player == 'w':
        message = "White to play and mate in four."
    else:
        message = "Black to play and mate in four."

    api = tweepy.API(auth)
    myID = api.me().id

    api.update_with_media(image,status=message)

    sleep(5)

    last_tweet = api.user_timeline(id=myID, count = 1)[0]

    sleep(500)
    api.update_status("@ChessDaily Solution:"+ ANSWER, in_reply_to_status_id=last_tweet.id)

def getKeys():
    f = open('/home/theodorc/dev/DailyPuzzles/keys.txt','r')
    l = []
    for line in f:
        l.append(line.rstrip())
    return l[0],l[1],l[2],l[3]

def query():
    conn = sqlite3.connect('/home/theodorc/dev/DailyPuzzles/mateIn4.db')
    c = conn.cursor()
    global ANSWER

    getCount = "SELECT number FROM count"
    count = c.execute(getCount).fetchone()
    newCount = count[0] + 1
    num = count[0]

    updateCount = f"UPDATE count SET number={newCount}"
    getFen = f"SELECT fen FROM puzzle WHERE id={num}"
    getPlayer = f"SELECT to_move FROM puzzle WHERE id={num}"
    getAnswer = f"SELECT solution FROM puzzle WHERE id={num}"
    ANSWER = c.execute(getAnswer).fetchone()[0]
    c.execute(updateCount)
    fen = c.execute(getFen).fetchone()
    player = c.execute(getPlayer).fetchone()
    conn.commit()
    conn.close()
    return fen[0],player[0]

main()





