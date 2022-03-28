from mcdreforged.api.all import *
from typing import Dict
from .data import ColorData

PREFIX = '!!color'

color_data: ColorData = None


def on_load(server: PluginServerInterface, old):
    global color_data
    color_data = ColorData(server)
    server.register_help_message(PREFIX, '改变用户名颜色')
    server.register_command(
        Literal(PREFIX).then(
            Literal('create').then(Text('color').runs(create))
        )
        .then(
            Literal('add').then(Text('player').then(Text('color').runs(add)))
        )
        .then(
            Literal('set').then(Text('color').runs(set_color))
        )
        .then(
            Literal('delete').then(
                Text('player').then(Text('color').runs(delete)))
        )
        .then(
            Literal('list').runs(list_all)
        )
    )


def create(src: CommandSource, ctx: Dict):
    global color_data
    if src.has_permission_higher_than(3):
        try:
            color_data.create(
                src.get_server().as_plugin_server_interface(), ctx['color'])
        except RuntimeError as e:
            src.reply(str(e))
    else:
        src.reply('权限不足')


def add(src: CommandSource, ctx: Dict):
    global color_data
    try:
        color_data.add_player(src.get_server().as_plugin_server_interface(),
                              ctx['player'], ctx['color'])
        src.reply('成功添加{}到{}中'.format(ctx['player'], ctx['color']))
    except RuntimeError as e:
        src.reply(str(e))


def set_color(src: CommandSource, ctx: Dict):
    global color_data
    if not src.is_player:
        src.reply('只有玩家才可以执行该命令')
        return
    # src is PlayerCommandSource
    try:
        color_data.set_color(
            src.get_server().as_plugin_server_interface(), src.player, ctx['color'])
    except RuntimeError as e:
        src.reply(str(e))


def delete(src: CommandSource, ctx: Dict):
    global color_data
    if src.has_permission_higher_than(3):
        try:
            color_data.delete_player(src.get_server().as_plugin_server_interface(),
                                     ctx['player'], ctx['color'])
            src.reply('成功从{}中移除{}'.format(ctx['color'], ctx['player']))
        except RuntimeError as e:
            src.reply(str(e))
    else:
        src.reply('权限不足')


def list_all(src: CommandSource, ctx: Dict):
    # stub
    global color_data
    src.reply(list(color_data.data.keys()))
