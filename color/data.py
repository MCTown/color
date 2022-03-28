import json
import os.path

from mcdreforged.api.all import PluginServerInterface

FILE = 'color.json'
COLORS = ('aqua', 'black', 'blue', 'dark_aqua', 'dark_blue', 'dark_gray', 'dark_green',
          'dark_purple', 'dark_red', 'gold', 'gray', 'green', 'light_purple', 'red', 'white', 'yellow')


class ColorData:

    # self.data: color -> [player_names]
    def __init__(self, server: PluginServerInterface):
        try:
            self._reload(server)
        except FileNotFoundError:
            self.data = {}
            self.save(server)

    def _reload(self, server: PluginServerInterface):
        with open(os.path.join(server.get_data_folder(), FILE), 'r') as f:
            self.data = json.loads(f.read())

    def _check_color_exists(self, color: str):
        if not color in self.data:
            raise RuntimeError('{}不存在'.format(color))

    def save(self, server: PluginServerInterface):
        with open(os.path.join(server.get_data_folder(), FILE), 'w') as f:
            f.write(json.dumps(self.data))

    def create(self, server: PluginServerInterface, color: str):
        if not color in COLORS:
            raise RuntimeError('输入{}无效，有效的输入为{}'.format(color, COLORS))
        if color in self.data:
            raise RuntimeError('{}已经存在'.format(color))
        else:
            server.execute('team add _{}'.format(color))
            server.execute('team modify _{} color {}'.format(color, color))
            self.data[color] = []
            self.save(server)

    def add_player(self, server: PluginServerInterface, player: str, color: str):
        self._check_color_exists(color)
        if player in self.data[color]:
            raise RuntimeError('{}已经在{}组中'.format(player, color))
        self.data[color].append(player)
        self.save(server)

    def delete_player(self, server: PluginServerInterface, player: str, color: str):
        self._check_color_exists(color)
        if not player in self.data[color]:
            raise RuntimeError('{}已经不在{}中'.format(player, color))
        self.data[color].remove(player)
        self.save(server)

    def set_color(self, server: PluginServerInterface, player: str, color: str):
        self._check_color_exists(color)
        if not player in self.data['color']:
            raise RuntimeError('玩家{}不在{}中'.format(player, color))
        server.execute('team join _{} {}'.format(color, player))
