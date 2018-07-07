import socket
import random

from Qt import QtCore

from ChitChat.networking.utils import (
    Message, ChatAppMessageError, BROADCAST_PORT, BROADCAST_ADDR
)
from ChitChat.networking.broadcast import BroadcastPacketPoster


class BroadcastPacketListener(QtCore.QObject):
    response = QtCore.Signal(str, str)

    def __init__(self, user, parent=None):
        super(BroadcastPacketListener, self).__init__(parent)
        self.stop = False
        self.socket = None
        self.broadcaster = BroadcastPacketPoster(user)

    @QtCore.Slot(str)
    def setName(self, name):
        self.broadcaster.setName(name)

    @QtCore.Slot()
    def process(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind(
                (BROADCAST_ADDR, BROADCAST_PORT)
            )
        except socket.error:
            port = BROADCAST_PORT
            port -= random.randint(1, 50)
            print("Port %d in use. Retrying on %d" % (BROADCAST_PORT, port))
            self.socket.bind(
                (BROADCAST_ADDR, port)
            )

        while not self.stop:
            data, (host, port) = self.socket.recvfrom(1024)
            try:
                message = Message.from_str(data)
                print(
                    "Received message from \"{u}\": \"{host}\"".format(
                        u=message.user, host=message.hostname
                    )
                )
                self.response.emit(message.user, message.hostname)
                self.broadcaster.broadcast()
            except ChatAppMessageError as err:
                print("ERROR: \"{err}\"".format(err=err))

    @QtCore.Slot()
    def exit_slot(self):
        self.stop = True

