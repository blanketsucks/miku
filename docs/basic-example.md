# Basic Usage

Fetching an anime
```py
import miku
import asyncio

async def main():
    async with miku.Client() as client:
        paginator = client.anime('Gurren Lagann')

        async for page in paginator:
            for anime in page:
                print(anime.name.native)

asyncio.run(main())
```

Fetching a character
```py
import miku
import asyncio

async def main():
    async with miku.Client() as client:
        paginator = client.character('Koyomi Araragi')

        async for page in paginator:
            for character in page:
                print(character.name.full)

asyncio.run(main())
```

Using your own `aiohttp.ClientSession` object
```py
import miku
import asyncio
import aiohttp

async def main():
    session = aiohttp.ClientSession()
    
    async with miku.Client.from_session(session) as client:
        paginator = client.anime('Gurren Lagann')

        async for page in paginator:
            for anime in page:
                print(anime.name.native)

asyncio.run(main())
```
