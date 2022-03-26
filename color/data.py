import json
import os.path

from mcdreforged.api.all import PluginServerInterface

FILE = 'color.json'

class ColorData:

    # self.data: color -> [player_names]
    def __init__(self, server: PluginServerInterface):
        try:
            with open(os.path.join(server.get_data_folder(), FILE), 'r') as f:
                self.data = json.loads(f.read())
        except FileNotFoundError:
            self.data = {}
            self.save(server)
    
    def save(self, server: PluginServerInterface):
        with open(os.path.join(server.get_data_folder(), FILE), 'w') as f:
            f.write(json.dumps(self.data))
    
    def create(self, server: PluginServerInterface, color: str):
        if color in self.data:
            raise RuntimeError('{}已经存在'.format(color))
        else:
            server.execute('team add _{}'.format(color))
            server.execute('team modify _{} color {}'.format(color, color))
            self.data[color] = []
            self.save(server)
    
    def add_user(self, server: PluginServerInterface, player: str, color: str):
        if not color in self.data:
            raise RuntimeError('{}不存在'.format(color))
        if player in self.data[color]:
            raise RuntimeError('{}已经在{}组中'.format(player, color))
        self.data[color].append(player)
        self.save(server)
    
    def change_color(self, server: PluginServerInterface, player: str, color: str):
        if not color in self.data:
            raise RuntimeError('颜色组{}还不存在'.format(color))
        if not player in self.data['color']:
            raise RuntimeError('玩家{}不在{}中'.format(player, color))
        server.execute('team join _{} {}'.format(color, player))
