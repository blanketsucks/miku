# Miku

An Unofficial AniList python API wrapper.

## Installation

**Python 3.8 is required for the installation.**
Installation is done via git:
```py
# Linux/MacOS
python3 -m pip install -U git+https://github.com/blanketsucks/miku

# Windows
py -3 -m pip install -U git+https://github.com/blanketsucks/miku
```
-----

## Basic Examples

Fetching an anime
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        anime = await client.fetch_anime('Gurren Lagann')
        print(anime)

asyncio.run(main())
```

Fetching a manga (this includes light novels)
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        manga = await client.fetch_manga('Bakemonogatari')
        print(manga)

asyncio.run(main())
```

Fetching a character
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        character = await client.fetch_character('Miku Nakano')
        print(character)

asyncio.run(main())
```

Searching for multiple animes
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        animes = await client.animes('5-toubun no Hanayome')
        print(animes)

asyncio.run(main())
```

Using the `miku.Paginator` class
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        paginator = client.animes('Boku no Hero Academia')

        async for page in paginator:
            for anime in page:
                print(anime)

asyncio.run(main())
```
