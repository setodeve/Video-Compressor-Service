import socket
import os
import json
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
                status = self.file_check(file_name)
                if status:
                    break
            message_req = {}
            message_req["file_size"] = self.file_size
            self.send_json_message(message_req)

            with open(file_name, "rb") as file:
                file_data = file.read(self.size)
                while file_data:
                    self.sock.send(file_data)
                    file_data = file.read(self.size)

            message_res = self.receive_json_message()

            if message_res["status"] == self.POSITIVE:
                print("Succeeded to upload video")
            else:
                print("Failed to upload video")

        except Exception as err:
            print("Error: " + str(err))

    def send_json_message(self, message):
        json_data = json.dumps(message).encode("utf-8")
        self.sock.sendto(json_data, self.setinfo)

    def receive_json_message(self):
        message_recv = self.sock.recv(self.text_size).decode("utf-8")
        return json.loads(message_recv)

    def file_check(self, file_name):
        file_status = os.stat(file_name)
        if file_status.st_size > self.MAX_SIZE:
            print("Filesize can not be over 4GB")
            return False
        self.file_size = file_status.st_size
        _, ext = os.path.splitext(file_name)
        if ext != ".mp4":
            print("Extention is not mp4")
            return False
        return True


Client().upload_video()
