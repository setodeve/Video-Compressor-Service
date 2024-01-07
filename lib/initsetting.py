import sys
import socket

sys.dont_write_bytecode = True


class InetSetting:
    POSITIVE = 0
    NEGATIVE = 1

    def __init__(self, address, port, type) -> None:
        self.address = address
        self.port = port
        self.setinfo = (address, port)
        self.sock = socket.socket(socket.AF_INET, type)
        self.size = 1400
        self.text_size = 1024
        self.file_type = ""
        self.sock.settimeout(20)
        self.file_size = 0
