# clashroyaleapi v0.1.1

Note: Clash Royale's official API will be added into the library in the next version.

A Python 3.7 wrapper for [RoyaleAPI](https://royaleapi.com/),
based on [Jeff](https://github.com/jeffffc)'s [crpy](https://test.pypi.org/project/crpy/). (WIP)

The wrapper's code style is inspired by
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and
[Telethon](https://github.com/LonamiWebs/Telethon) and attempts to improve the existing Python wrappers for RoyaleAPI.

You are recommended to read [RoyaleAPI's documentation](https://docs.royaleapi.com)
before using this wrapper.

Documentation is to be written. For now, you may reference the
[short examples](https://github.com/Tr-Jono/clashroyaleapi#short-examples-of-using-the-wrapper) below.

## Installation
The project is on [PyPI](https://pypi.org/project/clashroyaleapi/).
```
pip install clashroyaleapi
```

## Obtaining Developer Key
Follow [these instructions](https://docs.royaleapi.com/#/authentication?id=generating-new-keys)
to obtain your developer key.

## Currently Supported Methods
Tuples, dicts, sets and generators can be used instead of lists.
```
client.get_player(player_tag)  # alias: client.get_players()
client.get_player_battles(player_tag)  # alias: client.get_players_battles()
client.get_player_chests(player_tag)  # alias: client.get_players_chests()
client.get_clan(clan_tag)  # alias: client.get_clans()
client.get_version()
```

## Short examples of using the wrapper
Note: Player/Clan/Tournament tags will be "corrected" and validated before requesting the API.
### Example 1: `with` statement
```python
import royaleapi

with royaleapi.RoyaleAPIClient("YOUR_DEVELOPER_KEY") as client:
    p = client.get_player("2RQJ0OYYC")
    print(p.name, p.stats.favorite_card.name, p.deck[0].name, sep=", ")
    c1, c2 = client.get_clans(("c9c8pcp", "#8LYRRV2"))
    print(c1.badge == c2.badge, c1.location == c2.location)
    print([(c.name, c.members[0].name, c.members[0].trophies) for c in (c1, c2)])

# (My) Results:
# Trainer Jono, Golem, The Log
# False True
# [('新香港部落123', '花果山劉德華', 5073), ('香港部落·二部', 'Gnuelnam', 4479)]
```
### Example 2: Using cached data
```python
import time
from royaleapi import RoyaleAPIClient

client = RoyaleAPIClient("YOUR_DEVELOPER_KEY", use_cache=True)
player_tag = "9YJ2RR8G"
t1 = time.time()
p1 = client.get_player(player_tag)
t2 = time.time()
p2 = client.get_player(player_tag)
t3 = time.time()
p3 = client.get_player(player_tag, use_cache=False)
t4 = time.time()
print(t2 - t1, t3 - t2, t4 - t3, p1 == p2 == p3)

# (My) Results
# 2.3867766857147217 0.28074216842651367 1.4506447315216064 True

# The first call takes the longest time since the data is not cached locally or on RoyaleAPI's server.
# The second call takes the shortest time since the data is cached locally.
# The third call takes less time than the first call since that data is cached on RoyaleAPI's server.
```
