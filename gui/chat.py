from Qt import QtWidgets, QtCore

from ChitChat.gui.message_log import MessageLogWidget
from ChitChat.gui.input_widget import InputWidget

from ChitChat.networking.broadcast import PacketPoster
# Maybe no networking in here? This is gui code yo..


class ChatWindow(QtWidgets.QWidget):
    messageSendRequest = QtCore.Signal(str, str, str)

    def __init__(self, username, host, parent=None):
        super(ChatWindow, self).__init__(parent)
        self.username = username
        self.host = host

        self.setLayout(QtWidgets.QVBoxLayout())
        self.message_log_widget = MessageLogWidget(self)
        self.input_widget = InputWidget(self)
        self.input_widget.returnKeyPressed.connect(self.sendText)
        self.layout().addWidget(self.message_log_widget)
        self.layout().addWidget(self.input_widget)

    def sendText(self):
        self.message_log_widget.addLine(self.username, self.input_widget.text())
        self.messageSendRequest.emit(
            self.username,
            self.host,
            self.input_widget.text()
        )
        self.input_widget.clear()


class ChatTab(QtWidgets.QTabWidget):
    messageSendRequest = QtCore.Signal(str, str, str)

    def __init__(self, parent=None):
        super(ChatTab, self).__init__(parent)

        self.chats = {}
        self.setMinimumWidth(400)

    def addChat(self, user, host):
        chat = ChatWindow(user, host, self)
        self.chats[user] = chat
        index = self.addTab(chat, "%s@%s" % (user, host))
        self.setCurrentIndex(index)
        chat.messageSendRequest.connect(self.send_message)

    @QtCore.Slot(str, str, str)
    def send_message(self, name, host, message):
        self.messageSendRequest.emit(name, host, message)
