import socket
import os
import json
from lib.initsetting import InetSetting


class Client(InetSetting):
    def __init__(self) -> None:
        super().__init__("0.0.0.0", 8080, socket.SOCK_STREAM)
        self.sock.connect(self.setinfo)
        self.MAX_SIZE = 2**47  # 128TB
        self.file_name = ""
        self.type = ""
        self.cmd = ""
        self.input_file_type = ""
        self.output_file_type = ""
        self.option = ""

    def upload_video(self):
        try:
            while True:
                file_name = input("Enter video file name ex.'video.mp4' : ")
                self.file_name = file_name
                status = self.file_check(file_name)
                if status:
                    break

            self.start_process()

            message_req = {}
            message_req["file_size"] = self.file_size
            message_req["input_file_type"] = self.input_file_type
            message_req["output_file_type"] = self.output_file_type
            message_req["type"] = self.type
            message_req["cmd"] = self.cmd
            message_req["option"] = self.option

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

            print("Processing....")

            message_res = self.receive_json_message()
            if message_res["status"] == self.POSITIVE:
                print("Succeeded to process video")
                print("Stored Processed file in " + message_res["file_path"])
            else:
                print("Failed to process video")

        except Exception as err:
            print("Error: " + str(err))

    def file_check(self, file_name):
        file_status = os.stat(file_name)
        if file_status.st_size > self.MAX_SIZE:
            print("Filesize can not be over 128TB")
            return False
        _, ext = os.path.splitext(file_name)
        self.input_file_type = ext
        self.file_size = file_status.st_size
        return True

    def start_process(self):
        while True:
            option = int(
                input(
                    "動画の処理方法を1~5から選択してください\n"
                    + "  1 : 動画の圧縮\n"
                    + "  2 : 動画の解像度変更\n"
                    + "  3 : 動画のアスペクト比変更\n"
                    + "  4 : 動画からの音声変換\n"
                    + "  5 : 特定時間範囲のGIF/WEBM作成\n"
                )
            )
            self.cmd = "ffmpeg -i"
            if option == 1:
                self.type = "compress"
                self.output_file_type = input(
                    "Enter (filename) extension after processing ex.'.mp4'  : "
                )
                break
            elif option == 2:
                self.type = "resolution"
                print("Enter width(px) and height(px) for video resolution")
                width = input("Enter width(px) ex. 1280 : ")
                height = input("Enter height(px) ex. 720 : ")
                self.output_file_type = input(
                    "Enter (filename) extension after processing ex.'.mp4'  : "
                )
                self.option = "-s " + width + "x" + height
                break
            elif option == 3:
                print("Enter width and height to change aspect")
                width = input("Enter width ex. 16 : ")
                height = input("Enter height ex. 9 : ")
                self.type = "aspect_ratio"
                self.output_file_type = input(
                    "Enter (filename) extension after processing ex.'.mp4'  : "
                )
                tmp = width + "/" + height
                self.option = (
                    "-vf "
                    + f"'pad=width=max(iw\,ih*({tmp})):height=ow/({tmp}):x=(ow-iw)/2:y=(oh-ih)/2'"
                )
                break
            elif option == 4:
                self.type = "mp3"
                self.output_file_type = ".mp3"
                break
            elif option == 5:
                self.type = "gif"
                self.output_file_type = ".gif"
                start = input("Enter start time for creating gif ex.0 : ")
                end = input("Enter end time for creating gif ex.30 : ")
                time = f"-ss {start} -t {end}"
                self.option = time
                break

    def send_json_message(self, message):
        json_data = json.dumps(message).encode("utf-8")
        self.sock.sendto(json_data, self.setinfo)

    def receive_json_message(self):
        message_recv = self.sock.recv(self.text_size).decode("utf-8")
        return json.loads(message_recv)


client = Client()
client.upload_video()
