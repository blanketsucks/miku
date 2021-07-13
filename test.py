from miku import character
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        medias = await client.media('Darling in the FRANXX')
        
        for media in medias:
            print(media.is_licensed)
            print(media)

asyncio.run(main())