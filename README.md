# clashroyaleapi v0.2.2

A sync __Python 3.6+__ wrapper for [RoyaleAPI](https://royaleapi.com/). (WIP)

This wrapper's code style is inspired by
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot),
[Telethon](https://github.com/LonamiWebs/Telethon)
and [Jeff](https://github.com/jeffffc)'s [crpy](https://test.pypi.org/project/crpy/).
This wrapper attempts to provide an alternative which uses dataclasses to the existing Python wrappers for RoyaleAPI.

You are recommended to read [RoyaleAPI's documentation](https://docs.royaleapi.com) before using this wrapper
as the documentation for this wrapper is to be written. You may also reference the
[short examples](https://github.com/Tr-Jono/clashroyaleapi#short-examples-of-using-the-wrapper) below.

_This content is not affiliated with, endorsed, sponsored,
or specifically approved by Supercell and Supercell is not responsible for it.
For more information see [Supercell’s Fan Content Policy](http://supercell.com/en/fan-content-policy/)._

## Installation
This project is on [PyPI](https://pypi.org/project/clashroyaleapi/).
```
pip install clashroyaleapi
```

## Obtaining Developer Key
Follow [these instructions](https://docs.royaleapi.com/#/authentication?id=generating-new-keys)
to obtain your developer key.

## Currently Supported Methods
Methods with an alias indicate that multiple tags can be passed to them.
```python
client.get_player()            # alias: client.get_players()
client.get_player_chests()     # alias: client.get_players_chests()
client.get_player_battles()    # alias: client.get_players_battles()
client.get_clan()              # alias: client.get_clans()
client.get_clan_battles()
client.get_clan_war()
client.get_clan_war_log()
client.get_clan_history()
client.get_clan_tracking()     # alias: client.get_clans_tracking()
client.track_clan()            # alias: client.track_clans()
client.search_clans()
client.get_tournament()        # alias: client.get_tournaments()
client.get_known_tournaments()
client.search_tournaments()
client.get_top_players()
client.get_top_clans()
client.get_top_war_clans()
client.get_popular_players()
client.get_version()
client.get_health()
client.get_status()
client.get_endpoints()
```
Lists, tuples, dicts, sets and generators can be used when passing arguments to methods accepting multiple tags.
All of the following method calls are valid and return the same result.
```python
p = [tag1, tag2, tag3]

client.get_players(p)
client.get_players(*p)
client.get_players(tuple(p))
client.get_players(set(p))
client.get_players(dict.fromkeys(p))
client.get_players(tag for tag in p)
```

## Short examples of using the wrapper
Player/Clan/Tournament tags will be "corrected" and validated before requesting the API.
### ~~Example 1: `with` statement~~ (Will throw an error)
```python
import royaleapi

with royaleapi.RoyaleAPIClient("YOUR_DEVELOPER_KEY") as client:
    p = client.get_player("2RQJ0OYYC", timeout=100)
    print(p.name, p.stats.favorite_card.name, p.deck[0].name, sep=", ")
    c1, c2 = client.get_clans("c9c8pcp", "#8LYRRV2")
    print(c1.badge == c2.badge, c1.location == c2.location, sep=", ")
    print([(c.name, c.members[0].name, c.members[0].trophies) for c in (c1, c2)])

# My results:
# Trainer Jono, Golem, The Log
# False, True
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
print(t2 - t1, t3 - t2, t4 - t3, p1 == p2 == p3, sep=", ")

# My results
# 2.3867766857147217, 0.28074216842651367, 1.4506447315216064, True

# The first call takes the longest time since the data is not cached locally or on RoyaleAPI's server.
# The second call takes the shortest time since the data is cached locally.
# The third call takes less time than the first call since the data is cached on RoyaleAPI's server.
```

## Unfinished endpoints <sub><sup>(Ordered by priority)</sup></sub>
- `/tournament/global` (only `{"active": bool}`, if API authors finish the full endpoint, it will be implemented)
- `/constants` (figuring out how to implement)
- `/clan/:tag/history/weekly` (not working, API issue)
