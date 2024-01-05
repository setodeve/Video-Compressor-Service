import socket
from lib.initsetting import InetSetting


class Server(InetSetting):
    def __init__(self) -> None:
        super().__init__("0.0.0.0", 8080, socket.SOCK_STREAM)
        print("[TCP] Starting up on {} port {}".format(self.address, self.port))
        self.sock.bind(self.setinfo)
        self.sock.listen(1)

    def receive_video(self):
        try:
            filename = "output.mov"
            conn = self.sock.accept()
            with open(filename, "wb") as file:
                while True:
                    data = conn[0].recv(self.size)
                    if not data:
                        break
                    file.write(data)

            print("Success Upload")
        except Exception as err:
            print("Error: " + str(err))
        conn[0].close()


Server().receive_video()
