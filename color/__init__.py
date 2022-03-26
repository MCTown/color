from mcdreforged.api.all import *
from typing import Dict
from .data import ColorData

data: ColorData = None

def on_load(server: PluginServerInterface, old):
    global data
    data = ColorData(server)
    server.register_help_message('!!color', '改变用户名颜色')
    server.register_command(
        Literal('!!color').then(
            Literal('create').then(Text('color').runs(create))
        )
        .then(
            Literal('add').then(Text('player').then(Text('color').runs(add)))
        )
        .then(
            Literal('change').then(Text('color').runs(change))
        )
        .then(
            Literal('list').runs(list_all)
        )
    )


def create(src: CommandSource, ctx: Dict):
    global data
    if src.has_permission_higher_than(3):
        try:
            data.create(src.get_server().as_plugin_server_interface(), ctx['color'])
        except RuntimeError as e:
            src.reply(str(e))
    else:
        src.reply('权限不足')


def add(src: CommandSource, ctx: Dict):
    global data
    try:
        data.add_user(src.get_server().as_plugin_server_interface(), ctx['player'], ctx['color'])
        src.reply('成功添加{}到{}中'.format(ctx['player'], ctx['color']))
    except RuntimeError as e:
        src.reply(str(e))


def change(src: CommandSource, ctx: Dict):
    global data
    if not src.is_player:
        src.reply('只有玩家才可以执行该命令')
        return
    # src is PlayerCommandSource
    try:
        data.change_color(src.get_server().as_plugin_server_interface(), src.player, ctx['color'])
    except RuntimeError as e:
        src.reply(str(e))


def list_all(src: CommandSource, ctx: Dict):
    global data
    src.reply(list(data.data.keys()))
