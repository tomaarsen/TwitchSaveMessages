# TwitchSaveMessages
Twitch bot to save API information from chat messages and more in a database.

---
# Explanation
When the bot has started, it will start listening to chat messages in the channel listed in the settings.txt file. Beyond that, it listens to all other data Twitch sends us, and depending on our settings, stores it into a .db file. <b>This is meant for debugging purposes only.</b> Data is not stored efficiently.

---
# Database structure

| **Column**        | **Meaning** | 
| -------------------- | ----------- |
| full_message | Raw data from Twitch. |
| tags | All tags. These give information about a user, generally. Potentially empty | 
| command | The full command. |
| user | The user connected to the command. Optional. |
| type | The type of command. Important. |
| params | Parameters sent along with the command. Optional. |
| channel | The channel this command is sent in. Optional | 
| message | The message sent along. Optional. | 
| time | (Unix Epoch) Time at which the message was generated. |
| time_since_last | Time since previous message. | 

More information on the database structure [here](https://github.com/CubieDev/TwitchWebsocket), in the Output section.

---

# Requirements
* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "MessagesOnly": false
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| MessagesOnly         | Whether only chat messages should be stored. If false, messages like subscriptions, hosts, joins, parts, etc. will also be stored. | false |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# Note

Note that this bot creates a folder called "Logging" parallel to the folder this script exists in, where the logging information of this script is stored. This is perhaps not ideal for most users, but works well in my case, as it allows all of my bot's logs to be stored in one location, where I can easily access them.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
