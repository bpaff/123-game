from network import Listener, Handler, poll

handlers = {}  # map client handler to user name
plyrs = {'n': 0}

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)

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
        if msg['txt'] == 'rdy':
            self.do_send({'num_rdy': plyrs['n']})

Listener(8899, MyHandler)
while 1:
    poll(0.05)