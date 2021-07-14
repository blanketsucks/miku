# Basic Usage

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

Fetching a manga
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

Using your own `aiohttp.ClientSession` object
```py
import miku
import asyncio
import aiohttp

async def main():
    session = aiohttp.ClientSession()
    
    async with miku.AnilistClient.from_session(session) as client:
        anime = await client.fetch_anime('Kanojo mo Kanojo')
        print(anime)

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
        paginator = client.animes('5-toubun no Hanayome')

        async for page in paginator:
            for anime in page:
                print(anime)

asyncio.run(main())
```