from ui.PersistentDialog import *
from ui.SettingsDialog import SettingsDialog
from Configurate import Configurate


class MainWindow(PersistentDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = None
        self.setupUi()

    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        e.accept()

    def setupUi(self):
        mainLayot = QVBoxLayout()

        self.settingsBtn = QPushButton(self)
        self.settingsBtn.setText("Настройки")
        self.settingsBtn.clicked.connect(self.onOpenSettings)

        self.importBtn = QPushButton(self)
        self.importBtn.setText("Импорт")
        self.importBtn.clicked.connect(self.onImportData)

        self.createDataBtn = QPushButton(self)
        self.createDataBtn.setText("Создание данных")
        self.createDataBtn.clicked.connect(self.onCreateData)
        self.dataView = QTableView(self)
        # TODO:
        # Формирование модели для вьюшки из фрейма
        # self.dataView.setModel()

        mainLayot.addWidget(self.settingsBtn)
        mainLayot.addWidget(self.importBtn)
        mainLayot.addWidget(self.createDataBtn)
        mainLayot.addWidget(self.dataView)
        self.logWidget()
        mainLayot.addWidget(self.logTextBox)
        self.setLayout(mainLayot)

    def onOpenSettings(self):
        logging.info("Открытие настроек")
        self.settingsDialog = SettingsDialog()
        path = self.settingsDialog.exec_()
        if path:
            self.path = path

    def onImportData(self):
        logging.info("Импорт данных из файла")
        logging.info("Импорт таблицы")
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Окрыть таблицу", "", "Table Files (*.csv; *xlsx)")
        if not fileName:
            return

        columnNames, data = Configurate.getInfoFromCSV(fileName)

        dataModel = QStandardItemModel()
        for idx, name in enumerate(columnNames):
            dataModel.setHorizontalHeaderItem(idx, QStandardItem(name))

        for rowIndex, columnData in enumerate(data):
            rowData = []
            for info in columnData:
                rowData.append(QStandardItem(str(info)))

            dataModel.appendRow(rowData)

        self.dataView.setModel(dataModel)

    def onCreateData(self):
        logging.info("Создание данных")
        if self.path is None:
            columnsNames, data = Configurate.LoadFromJson()
        else:
            columnsNames, data = Configurate.LoadFromJson(self.path)

        dataModel = QStandardItemModel()
        for idx, name in enumerate(columnsNames):
            dataModel.setHorizontalHeaderItem(idx, QStandardItem(name))

        for rowIndex, columnData in enumerate(data):
            rowData = []
            for info in columnData:
                rowData.append(QStandardItem(str(info)))

            dataModel.appendRow(rowData)

        self.dataView.setModel(dataModel)
