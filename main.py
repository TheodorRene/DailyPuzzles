from time import sleep
import sqlite3
from sys import argv
from os import path
import subprocess
import tweepy
import config

#Global variable for the solution of todays puzzle
ANSWER = ""


#This command downloads the image from then fen into the picture "position.png"
def converting(fen):
    cmd = 'curl http://www.fen-to-image.com/image/36/single/coords/' + fen + ' | cat > /home/theodorc/dev/DailyPuzzles/position.png'
    subprocess.Popen(cmd, shell=True)

def main():
    #Get fen and color to move
    print("Querying the database")
    fen, player = query()
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
    c_k, c_s, a_k, a_s = getKeys()
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    image = 'position.png'

    if player == 'w':
        message = "White to play and mate in four. #Chess #Puzzle"
    else:
        message = "Black to play and mate in four. #Chess #Puzzle"

    api = tweepy.API(auth)
    myID = api.me().id

    api.update_with_media(image, status=message)

    #Wait until last tweet has gone through before postin reply
    sleep(5)

    last_tweet = api.user_timeline(id=myID, count=1)[0]

    print("Waiting 500 seconds until posting answer")
    sleep(250)
    print("....")
    sleep(250)
    print("Posting solution")
    api.update_status("@ChessDaily Solution:"+ ANSWER, in_reply_to_status_id=last_tweet.id)

#get keys and parsing
def getKeys():
    keys = [config.consumer_key, config.consumer_key_secret, config.access_token, config.access_token_secret]
    if '' in keys:
        raise Exception("You have not updated the config file. Please read the README before continuing")
    return keys[0], keys[1], keys[2], keys[3]

def query():
    if not path.exists("mateIn4.db"):
        raise Exception('Could not find database file')
    conn = sqlite3.connect('mateIn4.db')

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
    return fen[0], player[0]

main()
