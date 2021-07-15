import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        user = await client.fetch_user('blanketsucks')
        print(user.options.title_language)

asyncio.run(main())