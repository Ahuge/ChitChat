import socket

from Qt import QtCore

from ChitChat.networking.utils import (
    Message, MessageType, BROADCAST_ADDR, BROADCAST_PORT
) 


class PacketPoster(QtCore.QObject):
    finished = QtCore.Signal()
    _opts = [socket.SOL_SOCKET, socket.SO_BROADCAST, 1]
    DEFAULT_MSG_TYPE = MessageType.chat
    DEFAULT_ADDR = None
    DEFAULT_PORT = None

    def __init__(self, owner, addr=None, port=None, parent=None):
        super(PacketPoster, self).__init__(parent)
        self.owner = owner
        self.hostname = socket.gethostname()
        self.addr = addr or self.DEFAULT_ADDR
        self.port = port or self.DEFAULT_PORT
        self.sock = None

    def build_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.addr, self.port))

    def prepareMessage(self, message, message_type=None):
        return Message(
            user=self.owner,
            hostname=self.hostname,
            message_type=message_type or self.DEFAULT_MSG_TYPE,
            message=message,
        )

    @QtCore.Slot(str)
    def setName(self, name):
        self.owner = name

    @QtCore.Slot(str, int)
    def sendMessage(self, message, message_type=None):
        self.sock.setsockopt(*self._opts)
        formatted_message = self.prepareMessage(
            message=message, message_type=message_type
        ).to_str()

        print("Sending message \"{msg}\"".format(msg=formatted_message))
        self.sock.send(formatted_message)


class BroadcastPacketPoster(PacketPoster):
    _opts = [socket.SOL_SOCKET, socket.SO_BROADCAST, 1]
    DEFAULT_MSG_TYPE = MessageType.ehlo
    DEFAULT_ADDR = BROADCAST_ADDR
    DEFAULT_PORT = BROADCAST_PORT

    def build_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @QtCore.Slot()
    def broadcast(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = self.prepareMessage(message="")
        self.sock.sendto(message.to_str(), (self.addr, self.port))
        self.sock.close()
        self.finished.emit()

