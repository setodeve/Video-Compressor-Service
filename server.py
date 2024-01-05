import socket
import json
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
        filename = "output.mp4"
        try:
            conn = self.sock.accept()
            message_req = self.receive_json_message(conn[0])
            self.file_size = message_req["file_size"]

            with open(filename, "ab") as file:
                while self.file_size > 0:
                    data = conn[0].recv(self.size)
                    file.write(data)
                    self.file_size -= len(data)

        except Exception as err:
            print("Error: " + str(err))
            message_res["status"] = self.NEGATIVE

        self.send_json_message(conn[0], message_res)
        conn[0].close()

    def send_json_message(self, conn, message):
        json_data = json.dumps(message).encode("utf-8")
        conn.sendto(json_data, self.setinfo)

    def receive_json_message(self, conn):
        message_recv = conn.recv(self.text_size).decode("utf-8")
        return json.loads(message_recv)


Server().receive_video()
