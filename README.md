# clashroyaleapi

A [RoyaleAPI](https://royaleapi.com/) Python wrapper,
based on [jeffffc](https://github.com/jeffffc)'s [crpy](https://test.pypi.org/project/crpy/).

You are recommended to read [RoyaleAPI's documentation](https://docs.royaleapi.com/#/)
before using this wrapper.

Documentation will be written after at least half of the endpoints are coded.
For now, you may reference the short example below.

Note that only Python 3.6 is supported. Because of f-strings (there's like 10 or less?). Yay.

## Short example of using the wrapper

Follow [these instructions](https://docs.royaleapi.com/#/authentication?id=generating-new-keys)
to obtain your developer key.

```python
from crapi import Client

# Create a client to acces the methods. Fill in your developer key.
client = Client("DEV_KEY")


# Method to obtain a single Plyaer object. Use Client.get_players((tag1, tag2)) for obtaining mutiple player objects.
# Tags are automatically converted to uppercase, leading hashtag is removed and "O"s are replaced with "0"s.
player = client.get_player("#2rqjooyyc")

# Most key names are the same as those in received json, except keys that are
# camelCase (converted to snake_case), reserved Python keywords or other confusing words.
print(player.name, player.clan.donations_delta, player.stats.favorite_card.card_type)


# Method to obtain multiple Clan objects. Use Client.get_clan(tag) for obtaining a single Clan object.
# Keys & exclude also work, use an iterable to give multiple arguments to them.
newhkclan123, hkclansecond = client.get_clans(("C9C8PCP", "8LYRRV2"), exclude="members")

# You can compare objects directly.
print(newhkclan123.badge == hkclansecond.badge, newhkclan123.location == hkclansecond.location)

# Clan members are also objects.
for clan in newhkclan123, hkclansecond:
    print(f"Player with highest trophies in {clan.name}:\n"
          f"{clan.members[0].name} ({clan.members[0].trophies} trophies)")
```
