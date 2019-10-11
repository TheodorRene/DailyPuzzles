from main import log_in
from sys import argv

api = log_in()
api.update_status(argv[1])
