from network import Handler, poll

class MyHandler(Handler):
    
    def __init__(self, manager):
        host, port = 'localhost', 8888
        Handler.__init__(self, host, port)
        self.manager = manager
        #self.do_send({'join': myname})
        
    def on_close(self):
        pass
        
    def on_msg(self, msg):
        pass
            
    def send_msg(self, txt):
        pass
        #self.do_send({'speak': myname, 'txt': txt})
        
    def update(self):
        poll(0.01)
        
    def kill(self):
        self.close()  # will call on_close


self.gui = MyGUI(self)
self.network = MyHandler(self)
self.run()

self.keep_going = True
while self.keep_going:
    self.network.update()
    self.gui.update()
    self.gui.kill()
    self.network.kill()