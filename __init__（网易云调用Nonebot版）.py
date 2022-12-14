from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg,Arg
from nonebot.matcher import Matcher
from nonebot import logger
from nonebot import on_command
import aiohttp

async def get_song_id(key_word: str) -> int:
    url = 'http://127.0.0.1:3000/search?keywords='+key_word+''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song_data = await res.json()
            if res.status != 200:
                return 0
            return song_data['result']['songs'][0]['id']   
            
async def get_song_url(song_id:int):
    #看机器人文档的时候看到有人用了类似于vue的{}插值用法，我没能实现，不知道是怎么完成的
    url = 'http://127.0.0.1:3000/song/url?id='+str(song_id)+''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            song = await res.json()
            if song['code'] != 200:
                return None
            return song['data'][0]['url']

music_handler = on_command("网易云点歌",aliases={"文顺点歌"}, priority=5, block=True)

@music_handler.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    #这里应该是set key_word值
    if args:
        matcher.set_arg("key_word")

@music_handler.got("key_word", prompt="搜索的关键词是？")
async def _(bot: Bot, event: MessageEvent, key_word: Message = Arg()):
    song = key_word.extract_plain_text().strip()
    song_id = await get_song_id(song)
    if not song_id:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    song_mp4 = await (get_song_url(song_id))
    if not song_mp4:
        await music_handler.finish("没有找到这首歌！", at_sender=True)
    await music_handler.send(Message('[CQ:record,file='+song_mp4+']'))
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 来首 :{song}"
    )