
from TwitchWebsocket import TwitchWebsocket
import random, time, json, logging, os

from Log import Log
Log(__file__)

from Settings import Settings
from Database import Database

class SaveMessage:
    def __init__(self):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.messages_only = None
        self.last_message_t = time.time()
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

        self.db = Database()
        
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=["membership", "tags", "commands"],
                                  live=True)
        self.ws.start_bot()

    def setSettings(self, host, port, chan, nick, auth, messages_only):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
        self.messages_only = messages_only

    def message_handler(self, m):
        try:
            if m.type == "366":
                logging.info(f"Successfully joined channel: #{m.channel}")
            elif m.type == "PRIVMSG" or not self.messages_only:
                self.add_message_to_db(m, time.time() - self.last_message_t)
                self.last_message_t = time.time()
        except Exception as e:
            logging.error(e)
            
    def add_message_to_db(self, m, time_since_last):
        self.db.add_item(m.full_message, json.dumps(m.tags), m.command, m.user, m.type, m.params, m.channel, m.message, round(self.last_message_t), time_since_last)

if __name__ == "__main__":
    SaveMessage()
