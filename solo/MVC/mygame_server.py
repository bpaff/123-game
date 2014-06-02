from network import Listener, Handler, poll

handlers = {}  # map client handler to user name
plyrs = {'n': 0, 'rdy': 0}
lesgo = {}
all_scores = {}

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)

def find_top_score():
    top_score = 0
    for score in all_scores:
        if all_scores[score] > top_score:
            top_score = all_scores[score]
    return top_score


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        plyrs['n'] += 1
        print("a client has connected")
        print("number of clients now connected is " + str(plyrs['n']))
        self.do_send({'news': 'connected'})
        
    def on_close(self):
        del handlers[self]
        plyrs['n'] -= 1
        print("a client has disconnected")
        
    def on_msg(self, msg):
        if 'txt' in msg:
            if msg['txt'] == 'rdy':
                self.do_send({'num_rdy': plyrs['n']})
            elif msg['txt'] == 'lesgo':
                if self not in lesgo:
                  lesgo[self] = None
                if self in lesgo:
                    pass
                if len(lesgo) == 2:
                    broadcast({'news': 'START'})
        elif 'crt' in msg:
            all_scores[self] = msg['crt']
            evryscr = []
            broadcast({'top_score': str(find_top_score())})
            for player in all_scores:
                evryscr.append(all_scores[player])
            broadcast({'evryscr': evryscr})


Listener(8888, MyHandler)
while 1:
    poll(0.05)