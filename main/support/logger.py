# logs input
import datetime as dt

def log(message):
    with open('log.txt', 'a') as f:
        f.write(str(dt.datetime.now()) + " | "  + str(message) + "\n")