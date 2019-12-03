from main import log_in
from sys import argv

""" Simple script to tweet an update to the bot """
api = log_in()
api.update_status(argv[1])
