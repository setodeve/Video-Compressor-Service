import socket
import os
from lib.initsetting import InetSetting


class Client(InetSetting):
    def __init__(self) -> None:
        super().__init__("0.0.0.0", 8080, socket.SOCK_STREAM)
        self.sock.connect(self.setinfo)
        self.MAX_SIZE = 2**32  # 4GB

    def upload_video(self):
        try:
            while True:
                file_name = input("Enter file name : ")
                file_status = os.stat(file_name)

                if file_status.st_size > self.MAX_SIZE:
                    print("Filesize can not be over 4GB")
                else:
                    break

            with open(file_name, "rb") as file:
                file_data = file.read(self.size)
                while file_data:
                    self.sock.send(file_data)
                    file_data = file.read(self.size)
        except Exception as err:
            print("Error: " + str(err))


Client().upload_video()
