# clashroyaleapi

A Python 3.7 wrapper for [RoyaleAPI](https://royaleapi.com/),
based on [Jeff](https://github.com/jeffffc)'s [crpy](https://test.pypi.org/project/crpy/). (WIP)

The wrapper is inspired by [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) and
[Telethon](https://github.com/LonamiWebs/Telethon) and attempts to improve the existing Python wrappers for RoyaleAPI.

You are recommended to read [RoyaleAPI's documentation](https://docs.royaleapi.com)
before using this wrapper.

Documentation is to be written. For now, you may reference the
[short example](https://github.com/Tr-Jono/clashroyaleapi#short-example-of-using-the-wrapper) below.

## Short example of using the wrapper

Follow [these instructions](https://docs.royaleapi.com/#/authentication?id=generating-new-keys)
to obtain your developer key.

```
>>> from royaleapi import CRClient
>>> client = CRClient("YOUR_DEV_KEY")
>>> p = client.get_player("#2rqjooyyc")
>>> p.name, p.stats.favorite_card.name, p.current_deck[0].name
('Trainer Jono', 'Golem', 'The Log')
>>> c1, c2 = client.get_clans(("C9C8PCP", "8LYRRV2"))
>>> c1.badge == c2.badge, c1.location == c2.location
(False, True)
>>> [(c.name, c.members[0].name, c.members[0].trophies) for c in (c1, c2)]
[('新香港部落123', '花果山劉德華', 5076), ('香港部落·二部', 'BarcaAndy', 4407)]
```
