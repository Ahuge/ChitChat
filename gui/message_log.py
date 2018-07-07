from Qt import QtWidgets


class MessageLogWidget(QtWidgets.QPlainTextEdit):
    NL = "\n"

    def __init__(self, parent=None):
        super(MessageLogWidget, self).__init__(parent)
        self.setEnabled(False)
        self.text = ""

    def addLine(self, author="You", words=""):
        message = author + ": " + words
        self.text += message
        self.text += self.NL
        self.update_text()

    def update_text(self):
        self.setPlainText(self.text)

