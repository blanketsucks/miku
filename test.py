from miku import character
import miku
import asyncio

async def main():
    async with miku.AnilistClient() as client:
        characters = await client.character('nino nakano')
        nino = characters[0]

        print(nino._payload)


        
asyncio.run(main())