#!/home/theodorc/dev/Python-3.6.5/python

from time import sleep
import tweepy
import sqlite3
from sys import argv
import subprocess

#Global variable for the solution of todays puzzle
ANSWER = ""


#This command downloads the image from then fen into the picture "position.png"
def converting(fen):
    cmd = 'curl http://www.fen-to-image.com/image/36/single/coords/' + fen + ' | cat > /home/theodorc/dev/DailyPuzzles/position.png'
    subprocess.Popen(cmd,shell=True)

def main():
    #Get fen and color to move
    print("Querying the database")
    fen,player = query()
    #get image of position
    converting(fen)
    #wait until image is retrieved
    print("Waiting until FEN-image is retrieved")
    sleep(2)
    #Tweet 
    tweet(player)
    print("All done! Your tweet has been posted")

def tweet(player):
    #Get keys from text file
    c_k,c_s,a_k,a_s = getKeys()
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    image = '/home/theodorc/dev/DailyPuzzles/position.png'

    if player == 'w':
        message = "White to play and mate in four. #Chess #Puzzle"
    else:
        message = "Black to play and mate in four. #Chess #Puzzle"

    api = tweepy.API(auth)
    myID = api.me().id

    api.update_with_media(image,status=message)

    #Wait until last tweet has gone through before postin reply
    sleep(5)

    last_tweet = api.user_timeline(id=myID, count = 1)[0]

    print("Waiting 500 seconds until posting answer")
    sleep(250)
    print("....")
    sleep(250)
    print("Posting solution")
    api.update_status("@ChessDaily Solution:"+ ANSWER, in_reply_to_status_id=last_tweet.id)

#get keys and parsing
def getKeys():
    f = open('/home/theodorc/dev/DailyPuzzles/keys.txt','r')
    l = []
    for line in f:
        l.append(line.rstrip())
    return l[0],l[1],l[2],l[3]

def query():
    try:
        conn = sqlite3.connect('/home/theodorc/dev/DailyPuzzles/mateIn4.db')
    except sqlite3.Error as er:
        raise Exception("Could not find database file')

    c = conn.cursor()
    global ANSWER

    #Get the count from database, this has to update so new puzzle are fetched
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





