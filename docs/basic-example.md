# Basic Usage

Fetching animes
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        animes = await client.anime('Gurren Lagann')
        for anime in animes:
            print(anime)

asyncio.run(main())
```

Fetching mangas
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        mangas = await client.manga('Bakemonogatari')
        for manga in mangas:
            print(manga)

asyncio.run(main())
```

Fetching a character
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        characters = await client.character('Miku Nakano')
        for character in characters:
            print(character)

asyncio.run(main())
```

Using your own `aiohttp.ClientSession` object
```py
import miku
import asyncio
import aiohttp

async def main():
    session = aiohttp.ClientSession()
    
    async with miku.AnilistClient.from_session(session) as client:
        animes = await client.anime('Kanojo mo Kanojo')

        for anime in animes:
            print(anime)

asyncio.run(main())
```

Using the `miku.Paginator` class
```py
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        paginator = client.anime('5-toubun no Hanayome')

        async for page in paginator:
            for anime in page:
                print(anime)

asyncio.run(main())
```
