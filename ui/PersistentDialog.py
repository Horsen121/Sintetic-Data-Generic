from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTableView, QWhatsThis, QMessageBox,\
    QFormLayout, QLineEdit, QDoubleSpinBox, QMenu, QFileDialog
from ui.TextEditLogger import TextEditLogger
from ui.TextEditLogger import logging
from ui.InfoAboutDialog import InfoAboutDialog

class PersistentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("src/logo.png"))
        self.setWindowTitle("DataHack")

        self.settings = QSettings('SoItWillDo', 'SyntheticDataGenerator')

        self.resize(self.settings.value("size", QSize(600, 400)))
        self.move(self.settings.value("pos", QPoint(50, 50)))

    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        e.accept()

    def event(self, event):
        if event.type() == QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            infoDialog = InfoAboutDialog()
            infoDialog.exec_()

        return QDialog.event(self, event)

    def logWidget(self):
        logTextBox = TextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)
        logTextBox.widget.setFixedHeight(100)
        self.logTextBox = logTextBox.widget
