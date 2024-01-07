import socket
import json
import random
import string
import os
from lib.initsetting import InetSetting


class Server(InetSetting):
    def __init__(self) -> None:
        super().__init__("0.0.0.0", 8080, socket.SOCK_STREAM)
        print("[TCP] Starting up on {} port {}".format(self.address, self.port))
        self.sock.bind(self.setinfo)
        self.sock.listen(1)

    def receive_video(self):
        message_res = {}
        message_res["status"] = self.POSITIVE
        input_file = ""
        output_file = ""
        # Upload file
        try:
            conn = self.sock.accept()
            message_req = self.receive_json_message(conn[0])

            cmd = message_req["cmd"]
            output_file_type = message_req["output_file_type"]
            input_file_type = message_req["input_file_type"]
            type = message_req["type"]
            option = message_req["option"]
            self.file_size = message_req["file_size"]
            random_str = self.generate_random_str(5)
            input_file = "./input/" + type + "_" + random_str + input_file_type
            output_file = "./output/" + type + "_" + random_str + output_file_type

            with open(input_file, "wb") as file:
                while self.file_size > 0:
                    data = conn[0].recv(self.size)
                    file.write(data)
                    self.file_size -= len(data)

        except Exception as err:
            print("Error: " + str(err))
            message_res["status"] = self.NEGATIVE
        finally:
            self.send_json_message(conn[0], message_res)


        # Process file
        message_res = {}

        try:
            if type == "compress":
                message_res["type"] = "compress"
            elif type == "resolution":
                message_res["type"] = "resolution"
            elif type == "aspect_ratio":
                message_res["type"] = "aspect_ratio"
            elif type == "mp3":
                message_res["type"] = "mp3"
            print(cmd + " " + input_file + " " + option + " " + output_file)
            os.system(cmd + " " + input_file + " " + option + " " + output_file)
        except Exception as err:
            print("Error: " + str(err))
            message_res["status"] = self.NEGATIVE
        finally:
            message_res["file_path"] = output_file
            message_res["status"] = self.POSITIVE
            self.send_json_message(conn[0], message_res)

        conn[0].close()

    def send_json_message(self, conn, message):
        json_data = json.dumps(message).encode("utf-8")
        conn.sendto(json_data, self.setinfo)

    def receive_json_message(self, conn):
        message_recv = conn.recv(self.text_size).decode("utf-8")
        return json.loads(message_recv)

    def generate_random_str(self, n):
        randlst = [
            random.choice(string.ascii_letters + string.digits) for i in range(n)
        ]
        return "".join(randlst)


server = Server()
server.receive_video()
