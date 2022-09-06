
import json
import aiohttp
import asyncio
async def getSong_ID():
    url = 'http://127.0.0.1:7002/kuwo/search/searchMusicBykeyWord?key=zood'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print(res.status)
            #print(await res.text())
            song_data = await res.json()
            #今天花了一两个小时算是把python中跟js中很像的对象——字典给整的差不多明白了
            print(song_data['data']['list'][0]['rid'])
            song_id = song_data['data']['list'][0]['rid']
            return song_id
loop = asyncio.get_event_loop()
task = loop.create_task(getSong_ID())
loop.run_until_complete(task)
#使用异步函数中task的result()方法可以获取函数的返回值
print(task.result())
song_id = task.result()
async def getSong(song_id:int):
    #看机器人文档的时候看到有人用了类似于vue的{}插值用法，我没能实现，不知道是怎么完成的
    url = 'http://127.0.0.1:7002/kuwo/url?mid='+str(song_id)+'&type=music'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            print(res.status)
            #print(await res.json())
            song = await res.json()
            if song['code'] != 200:
                return None
            print(song['data']['url'])
loop = asyncio.get_event_loop()
task = loop.create_task(getSong(song_id))
loop.run_until_complete(task)