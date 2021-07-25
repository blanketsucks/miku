import miku

with miku.SyncAnilistClient() as client:
    anime = client.fetch_anime('Bakemonogatari')
    
    character = anime.characters.find(lambda character: character.name.full == 'Koyomi Araragi')
    print(character.apperances)

