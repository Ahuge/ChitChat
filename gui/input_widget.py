from Qt import QtWidgets, QtCore


class InputWidget(QtWidgets.QLineEdit):
    returnKeyPressed = QtCore.Signal()

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Return:
                self.returnKeyPressed.emit()
                return
        return super(InputWidget, self).keyPressEvent(event)

