import logging
from PyQt5.QtWidgets import QPlainTextEdit


class TextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        if "Answer received" in msg or "Command to send" in msg:
            return

        self.widget.appendPlainText(msg)
