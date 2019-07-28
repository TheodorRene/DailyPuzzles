from time import sleep
import sqlite3
from sys import argv
from os import path
import subprocess
import tweepy
import config
import logging

#Global variable for the solution of todays puzzle
ANSWER = ""


#This command downloads the image from then fen into the picture "position.png"
def converting(fen):
    logging.debug("retrieving image from fen: %s", fen)
    cmd = 'curl http://www.fen-to-image.com/image/36/single/coords/' + fen + ' > position.png'
    subprocess.Popen(cmd, shell=True)

def main():
    logging.basicConfig(filename='daily_puzzle.log',level=logging.DEBUG)
    logging.info("====STARTING NEW INSTANCE OF SCRIPT====")
    #Get fen and color to move
    fen, player = query()
    #get image of position
    converting(fen)
    sleep(5)
    #Tweet 
    tweet(player)
    logging.info("Tweet has been posted")
    logging.info("====END OF SCRIPT====")

def tweet(player):
    c_k, c_s, a_k, a_s = getKeys()
    logging.info("Connection to api")
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    image = 'position.png'

    if player == 'w':
        message = "White to play and mate in four. #Chess #Puzzle"
    else:
        message = "Black to play and mate in four. #Chess #Puzzle"

    api = tweepy.API(auth)
    myID = api.me().id
    if not config.IS_DEV:
        api.update_with_media(image, status=message)
        last_tweet = api.user_timeline(id=myID, count=1)[0]

    logging.info("Waiting 500 seconds until posting solution if in prod")
    if not config.IS_DEV:
        sleep(500)
    logging.info("Posting solution")
    if not config.IS_DEV:
        api.update_status("@ChessDaily Solution:"+ ANSWER, in_reply_to_status_id=last_tweet.id)

#get keys and parsing
def getKeys():
    logging.info("Retrieving keys from config file")
    keys = [config.consumer_key, config.consumer_key_secret, config.access_token, config.access_token_secret]
    if '' in keys:
        raise Exception("You have not updated the config file. Please read the README before continuing")
    return keys[0], keys[1], keys[2], keys[3]

def query():
    if not path.exists("mateIn4.db"):
        raise Exception('Could not find database file')
    logging.info("Connecting to database")
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
    logging.debug("Getting answer")
    ANSWER = c.execute(getAnswer).fetchone()[0]
    logging.info("Updating count")
    logging.debug("Current count: %s",ANSWER) 
    c.execute(updateCount)
    logging.info("Getting fen and player")
    fen = c.execute(getFen).fetchone()
    player = c.execute(getPlayer).fetchone()
    logging.debug("fen: %s player: %s", fen, player)
    logging.info("Closing connection")
    conn.commit()
    conn.close()
    return fen[0], player[0]

main()
