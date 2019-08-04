""" this module sleeps """
from time import sleep
import sqlite3
from os import path
import subprocess
import logging
import tweepy
import config
from create_board import gen_board

#Global variable for the solution of todays puzzle
ANSWER = ""


def converting(fen):
    """ takes in fen and retrieves image """
    logging.debug("retrieving image from fen: %s", fen)
    cmd = 'curl http://www.fen-to-image.com/image/36/single/coords/' + fen + ' > position.png'
    subprocess.Popen(cmd, shell=True)

def main():
    """ main function """
    logging.basicConfig(filename='daily_puzzle.log', level=logging.DEBUG)
    logging.info("====STARTING NEW INSTANCE OF SCRIPT====")
    #Get fen and color to move
    fen, player = query()
    #get image of position
    #converting(fen)
    gen_board(fen)
    sleep(5)
    #Tweet
    tweet(player)
    logging.info("Tweet has been posted")
    logging.info("====END OF SCRIPT====")


def tweet(player):
    """ it tweets """
    c_k, c_s, a_k, a_s = get_keys()
    logging.info("Connection to api")
    auth = tweepy.OAuthHandler(c_k, c_s)
    auth.set_access_token(a_k, a_s)
    image = 'position.png'

    if player == 'w':
        message = "White to play and mate in four. #Chess #Puzzle"
    else:
        message = "Black to play and mate in four. #Chess #Puzzle"

    api = tweepy.API(auth)
    my_id = api.me().id
    if not config.IS_DEV:
        api.update_with_media(image, status=message)
        last_tweet = api.user_timeline(id=my_id, count=1)[0]

    logging.info("Waiting 500 seconds until posting solution if in prod")
    if not config.IS_DEV:
        sleep(500)
    logging.info("Posting solution")
    if not config.IS_DEV:
        api.update_status("@ChessDaily Solution:"+ ANSWER, in_reply_to_status_id=last_tweet.id)

#get keys and parsing
def get_keys():
    """ Retrives keys from config file """
    logging.info("Retrieving keys from config file")
    keys = [config.consumer_key, config.consumer_key_secret, config.access_token, config.access_token_secret]
    if '' in keys:
        raise Exception("You have not updated the config file. Please read the README before continuing")
    return keys[0], keys[1], keys[2], keys[3]

def query():
    """ Does all the querying against the database """
    if not path.exists("mateIn4.db"):
        raise Exception('Could not find database file')
    logging.info("Connecting to database")
    conn = sqlite3.connect('mateIn4.db')

    database = conn.cursor()
    global ANSWER

    #Get the count from database, this has to update so new puzzle are fetched
    get_count = "SELECT number FROM count"
    count = database.execute(get_count).fetchone()
    new_count = count[0] + 1
    num = count[0]

    update_count = f"UPDATE count SET number={new_count}"
    get_fen = f"SELECT fen FROM puzzle WHERE id={num}"
    get_player = f"SELECT to_move FROM puzzle WHERE id={num}"
    get_answer = f"SELECT solution FROM puzzle WHERE id={num}"
    logging.debug("Getting answer")
    ANSWER = database.execute(get_answer).fetchone()[0]
    logging.info("Updating count")
    logging.debug("Current count: %s", ANSWER)
    database.execute(update_count)
    logging.info("Getting fen and player")
    fen = database.execute(get_fen).fetchone()
    player = database.execute(get_player).fetchone()
    logging.debug("fen: %s player: %s", fen, player)
    logging.info("Closing connection")
    conn.commit()
    conn.close()
    return fen[0], player[0]

main()
