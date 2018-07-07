from Qt import QtCore

from ChitChat.networking.listen import BroadcastPacketListener
from ChitChat.networking.broadcast import BroadcastPacketPoster


class BroadcastServerCore(QtCore.QObject):
    receiveMessage = QtCore.Signal(str, str)

    def __init__(self, name, parent=None):
        super(BroadcastServerCore, self).__init__(parent)

        self.listenerThread = QtCore.QThread(self)
        self.listener = BroadcastPacketListener(name)
        self.listener.moveToThread(self.listenerThread)

        self.broadcasterThread = QtCore.QThread(self)
        self.broadcaster = BroadcastPacketPoster(name)
        self.broadcaster.moveToThread(self.broadcasterThread)

        self.listenerThread.finished.connect(self.listener.exit_slot)
        self.listenerThread.started.connect(self.listener.process)
        self.listener.response.connect(self.new_user)

        self.broadcasterThread.started.connect(self.broadcaster.broadcast)
        self.broadcaster.finished.connect(self.broadcasterThread.quit)

        self.listenerThread.start()

    @QtCore.Slot()
    def refresh(self):
        print("Starting broadcasterThread")
        self.broadcasterThread.start()

    @QtCore.Slot(str)
    def setName(self, name):
        self.listener.setName(name)
        self.broadcaster.setName(name)

    @QtCore.Slot(str, str)
    def new_user(self, user, hostname):
        self.receiveMessage.emit(user, hostname)

