from ui.PersistentDialog import *


class InfoAboutDialog(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon("src/logo.png"))
        self.setWindowTitle("DataHack")
        self.setText('Данное приложение сделано командой "И ТАК СОЙДЕТ!"')
        self.setStandardButtons(QMessageBox.Ok)
