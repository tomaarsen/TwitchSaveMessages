
from TwitchWebsocket import TwitchWebsocket
import random, time, json, sqlite3, logging, os

class Logging:
    def __init__(self):
        # Either of the two will be empty depending on OS
        prefix = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1]) + "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1]) 
        prefix += "/Logging/"
        try:
            os.mkdir(prefix)
        except FileExistsError:
            pass
        log_file = prefix + os.path.basename(__file__).split('.')[0] + ".txt"
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # Spacer
        logging.info("")

class Settings:
    def __init__(self, bot):
        logging.debug("Loading settings.txt file...")
        try:
            # Try to load the file using json.
            # And pass the data to the GoogleTranslate class instance if this succeeds.
            with open("settings.txt", "r") as f:
                settings = f.read()
                data = json.loads(settings)
                bot.setSettings(data['Host'],
                                data['Port'],
                                data['Channel'],
                                data['Nickname'],
                                data['Authentication'],
                                data["MessagesOnly"])
                logging.debug("Settings loaded into Bot.")
        except ValueError:
            logging.error("Error in settings file.")
            raise ValueError("Error in settings file.")
        except FileNotFoundError:
            # If the file is missing, create a standardised settings.txt file
            # With all parameters required.
            logging.error("Please fix your settings.txt file that was just generated.")
            with open('settings.txt', 'w') as f:
                standard_dict = {
                                    "Host": "irc.chat.twitch.tv",
                                    "Port": 6667,
                                    "Channel": "#<channel>",
                                    "Nickname": "<name>",
                                    "Authentication": "oauth:<auth>",
                                    "MessagesOnly": False
                                }
                f.write(json.dumps(standard_dict, indent=4, separators=(',', ': ')))
            raise ValueError("Please fix your settings.txt file that was just generated.")

class Database:
    def __init__(self):
        self.create_db()
    
    def create_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Messages (
            full_message TEXT,
            tags TEXT,
            command TEXT,
            user TEXT,
            type TEXT,
            params TEXT,
            channel TEXT,
            message TEXT,
            time INTEGER,
            time_since_last REAL,
            PRIMARY KEY(full_message, time))
        """
        logging.debug("Creating Database...")
        self.execute(sql)
        logging.debug("Database created.")

    def execute(self, sql, values=None, fetch=False):
        with sqlite3.connect("Messages.db") as conn:
            cur = conn.cursor()
            if values is None:
                cur.execute(sql)
            else:
                cur.execute(sql, values)
            conn.commit()
            if fetch:
                return cur.fetchall()
    
    def add_item(self, *args):
        self.execute("INSERT INTO Messages(full_message, tags, command, user, type, params, channel, message, time, time_since_last) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", args)

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
    Logging()
    SaveMessage()
