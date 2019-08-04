# DailyPuzzles

---

Twitter bot for posting daily chess puzzles.
Simple project for learning simple database, Twitter api, text parsing and cron jobs. 

  * Pictures generated from http://www.fen-to-image.com/
  * Puzzles from http://wtharvey.com/ Only mate in four at the moment

---

## How to develop

* Make sure you have a python version >3.6
* Make a virtual enviroment and install tweepy
* Run makeDB.py
* Get developer keys for your account from https://developer.twitter.com/en.html
* Rename example_config.py to config.py and update constants
* Update cron_script with correct path and move it to /etc/cron.daily 
* ?????
* profit

## FAQ

* I lost track of the current puzzle 
  * SELECT id FROM puzzle WHERE solution LIKE "%{solution of last puzzle}%"

