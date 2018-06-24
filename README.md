# clashroyaleapi

A [RoyaleAPI](https://royaleapi.com/) Python wrapper,
based on [jeffffc](https://github.com/jeffffc)'s [crpy](https://test.pypi.org/project/crpy/).

You are suggested to read [RoyaleAPI's documentation](https://docs.royaleapi.com/#/) before using this wrapper.

Documentation will be written after at least half of the endpoints are coded.
For now, you may reference the short example below.

Note that only Python 3.6 is supported. Because of f-strings (there's like 10 or less?). Yay.

## Short example of using the wrapper

Follow [these instructions](https://docs.royaleapi.com/#/authentication?id=generating-new-keys)
to obtain your developer key.

```python
from crapi import Client


client = Client("DEV_KEY")  # Your developer key.

# Automatically converts to uppercase, removes hashtag and changes O to 0.
player = client.get_player("#2rqjooyyc")

# Most keys are the same as those in json, except keys that are
# camelCase (changed to snake_case), reserved Python keywords or confusing words.
print(player.name, player.clan.donations_delta, player.stats.favorite_card.card_type)


# Keys & exclude also work, use a iterable to give multiple arguments to them.
newhkclan123, hkclansecond = client.get_clans(("C9C8PCP", "8LYRRV2"), exclude="members")
# You can compare objects directly.

print(newhkclan123.badge == hkclansecond.badge, newhkclan123.location == hkclansecond.location)
for clan in newhkclan123, hkclansecond:
    print(f"Player with highest trophies in {clan}: {clan.members[0].name} ({clan.members[0].trophies} trophies)")
```