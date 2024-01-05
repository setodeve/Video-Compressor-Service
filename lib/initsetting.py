import sys
import socket

sys.dont_write_bytecode = True


class InetSetting:
    def __init__(self, address, port, type) -> None:
        self.address = address
        self.port = port
        self.setinfo = (address, port)
        self.sock = socket.socket(socket.AF_INET, type)
        self.size = 1400
