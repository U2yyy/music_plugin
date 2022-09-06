from music import get_song_id, get_song_url
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.typing import T_State
from services.log import logger
from nonebot import on_command


__zx_plugin_name__ = "点歌语音版"
__plugin_usage__ = """
usage：
    在线点歌，发送语音
    指令：
        来首 [歌名]
""".strip()
__plugin_des__ = "小文顺为你点歌"
__plugin_cmd__ = ["来首 [歌名]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 1.0
__plugin_author__ = "U2yyy"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["来首"],
}


music_handler = on_command("点歌", priority=5, block=True)


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
    await music_handler.send('[CQ:record,file='+song_mp4+']')
    logger.info(
        f"(USER {event.user_id}, GROUP "
        f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
        f" 来首 :{song}"
    )



