import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        for i in range(1000):
            anime = await client.fetch_anime('Gurren Lagann')
            print(anime)

asyncio.run(main())