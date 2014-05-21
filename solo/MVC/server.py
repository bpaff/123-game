"""
Server master:
The server is almighty. 
Every frame, it receives player inputs from clients,
executes these inputs to update the game state,
and sends the whole game state to all the clients for display. 
"""

from network import Listener, Handler, poll

all_players = {};

class MyHandler(Handler):
        
    def on_open(self):
        all_players[self] = {}
        print("A player has connected")
        
    def on_close(self):
        del all_players[self]
        
    def on_msg(self, data):
        all_players[self]['x'] = data['x']
        all_players[self]['y'] = data['y']

server = Listener(8888, MyHandler)

def serialize_players():
    poll()
    packaged_players = {}
    counter = 0
    for player in all_players:
        print(all_players[player]['y'])


def send_players():
    for player in all_players:
        for other_player in all_players:
            player.do_send(all_players)

while 1:
    poll(timeout = (0.02))
    serialize_players()
