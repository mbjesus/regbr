from configparser import ConfigParser


PARSER = ConfigParser()
PARSER.read('src/config.ini')

MONGO = 'options.mongodb'

def getMongoDbStrConn() -> str:
    return PARSER.get(MONGO,'connection')