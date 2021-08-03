import asyncio
import miku

async def main():
    async with miku.AsyncAnilistClient() as client:
        thread = await client.fetch_thread(5289)
        print(thread.to_dict())

asyncio.run(main())