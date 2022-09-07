from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot import logger
from nonebot import on_command
import json
import aiohttp
import asyncio


async def get_song_id(song_name: str) -> int:
    url = 'http://127.0.0.1:7002/kuwo/search/searchMusicBykeyWord?key='+song_name+''
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

music_handler = on_command("来首",aliases={"点歌"}, priority=5, block=True)

@music_handler.handle()
async def handle_first_receive(state: T_State, arg: Message = CommandArg()):
    #将命令语句格式化并存入state字典中
    if args := arg.extract_plain_text().strip():
        state["song_name"] = args

@music_handler.got("song_name", prompt="歌名是？")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    song = state["song_name"]
    song_id = await get_song_id(song)
    if not song_id:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    song_mp4 = await (get_song_url(song_id))
    if not song_mp4:
        await music_handler.finish("没有找到这首歌！" at_sender=True)
    await music_handler.send(Message('[CQ:record,file='+song_mp4+']'))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 来首 :{song}"
    )