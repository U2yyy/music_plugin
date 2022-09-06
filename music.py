import json
import aiohttp
import asyncio

async def get_song_id(song_name: str) -> int:
    url = 'http://127.0.0.1:7002/kuwo/search/searchMusicBykeyWord?key=zood'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song_data = await res.json()
            if res.status != 200:
                return 0
            return song_data['data']['list'][0]['rid']   
            
async def get_song_url(song_id:int):
    #看机器人文档的时候看到有人用了类似于vue的{}插值用法，我没能实现，不知道是怎么完成的
    url = 'http://127.0.0.1:7002/kuwo/url?mid='+str(song_id)+'&type=music'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song = await res.json()
            if song['code'] != 200:
                return None
            return song['data']['url']