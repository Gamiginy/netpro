import socket

class Client:

    def __init__(self):
        self.name = None
        self.soc = None
        self.position = []

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_socket(self, socket):
        self.soc = socket

    def enter(self, number):
        self.position.append(number)

    def leave(self):
        self.position.pop()
        if len(self.position) == 0:
            return -1
        else:
            return self.position[len(self.position)-1]
