import asyncio
import miku

def sync_client():
    client = miku.SyncAnilistClient()
    animes = client.animes('Bakemonogatari').collect()
    print(animes)

async def async_client():
    client = miku.AsyncAnilistClient()
    medias = await client.animes('Bakemonogatari')
    print(medias)
    
async def main():
    sync_client()
    await async_client()

asyncio.run(main())