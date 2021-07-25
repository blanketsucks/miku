import asyncio
import miku

def sync_client():
    client = miku.SyncAnilistClient()
    paginator = client.animes('Bakemonogatari')

    for page in paginator:
        for media in page:
            print(media.title)

    client.close()

async def async_client():
    client = miku.AsyncAnilistClient()
    paginator = client.medias('Bakemonogatari')
    
    async for page in paginator:
        for media in page:
            print(media.title)

    await client.close()

async def main():
    sync_client()
    await async_client()

asyncio.run(main())


