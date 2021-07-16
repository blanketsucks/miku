from miku.character import Character
from miku.media import Anime
from miku.paginator import Data
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        statistics = await client.fetch_site_statistics()
        print(statistics.anime)

asyncio.get_event_loop().run_until_complete(main())