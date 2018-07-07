from Qt import QtWidgets, QtCore, QtGui


class UserList(QtWidgets.QWidget):
    request_open_chat = QtCore.Signal(str, str)
    request_refresh_user_list = QtCore.Signal()
    open_brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
    close_brush = None

    def __init__(self, parent=None):
        super(UserList, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.user_list_widget = QtWidgets.QListWidget()
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self._map = {}  # Users to addresses

        self.layout().addWidget(self.user_list_widget)
        self.layout().addWidget(self.refresh_button)

        self._refresh()

        self.user_list_widget.itemDoubleClicked.connect(self._open_chat_user)
        self.refresh_button.clicked.connect(self._refresh)

    def mark_user_open(self, user):
        users = self.user_list_widget.findItems(user, QtCore.Qt.MatchExactly)
        for useritem in users:
            useritem.setBackground(self.open_brush)

    def mark_user_close(self, user):
        users = self.user_list_widget.findItems(user, QtCore.Qt.MatchExactly)
        for useritem in users:
            useritem.setBackground(self.close_brush)

    def _open_chat_user(self, list_widget_item):
        host = self._map[list_widget_item.text()]

        self.request_open_chat.emit(list_widget_item.text(), host)

    def _refresh(self):
        self.request_refresh_user_list.emit()

    @QtCore.Slot(str, str)
    def addUser(self, name, address):
        found = False
        if name in self._map:
            items = self.user_list_widget.findItems(name, QtCore.Qt.MatchExactly)
            if len(items):  # If it's already there, update address.
                found = True

        if not found:
            print("New user: {name} @ {addr}".format(name=name, addr=address))
            self.user_list_widget.addItem(name)
        self._map[name] = address
        self.close_brush = self.user_list_widget.item(0).background()

