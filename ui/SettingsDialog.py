from ui.PersistentDialog import *
from ui.ColumnInfoDialog import ColumnInfoDialog
from managers.JsonManager import JsonManager
from managers.ColumnsManager import Columns
from entities.ColumnItem import ColumnItem
import sys


class SettingsDialog(PersistentDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.setupJsonManager()
        self.setupModel()

    def setupUi(self):
        mainLayout = QVBoxLayout()

        self.loadSettingsBtn = QPushButton(self)
        self.loadSettingsBtn.setText('Загрузить конфигурацию')
        self.loadSettingsBtn.clicked.connect(self.onLoadSettings)

        self.configView = QTableView(self)
        self.configView.setContextMenuPolicy(Qt.DefaultContextMenu)

        # Settings
        formLayout = QFormLayout()
        self.tableName = QLineEdit()
        self.rowCount = QDoubleSpinBox()
        self.rowCount.setDecimals(0)
        self.rowCount.setMinimum(0)
        self.rowCount.setMaximum(sys.maxsize)

        formLayout.addRow("Название таблицы: ", self.tableName)
        formLayout.addRow("Количество строк: ", self.rowCount)

        self.saveSettingsBtn = QPushButton(self)
        self.saveSettingsBtn.setText('Сохранить конфигурацию')
        self.saveSettingsBtn.clicked.connect(self.onSaveSettings)

        mainLayout.addWidget(self.loadSettingsBtn)
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.configView)
        mainLayout.addWidget(self.saveSettingsBtn)

        self.setLayout(mainLayout)

    def contextMenuEvent(self, event):
        hheader, vheader = self.configView.horizontalHeader(), self.configView.verticalHeader()
        position = event.globalPos()
        row = vheader.logicalIndexAt(vheader.mapFromGlobal(position))
        column = hheader.logicalIndexAt(hheader.mapFromGlobal(position))

        menu = QMenu(self)
        if row < 0 or column < 0:
            createColumnAction = menu.addAction("Создать колонку")
            createColumnAction.triggered.connect(lambda:
                                             self.onColumnCreate()
                                             )
        else:
            item = self.model.item(row, column)
            columnId = item.data(404)
            columnItem = self.findColumnItem(columnId)
            propertyAction = menu.addAction("Свойства")
            propertyAction.triggered.connect(lambda:
                                             self.onPropertyDialogShow(columnItem)
                                             )
            removeColumnAction = menu.addAction("Удалить колонку")
            removeColumnAction.triggered.connect(lambda:
                                             self.onRemoveColumn(columnItem)
                                             )

        menu.exec_(position)

    def onRemoveColumn(self, columnItem):
        columns = Columns.getInstance()
        columns.columns.remove(columnItem)
        self.onUpdateModel(False)

    def onColumnCreate(self):
        columnName = self.model.columnCount()
        columnInfoDialog = ColumnInfoDialog(ColumnItem(columnName))
        ret = columnInfoDialog.exec_()
        if ret:
            self.onUpdateModel(False)

    def onPropertyDialogShow(self, columnItem):
        columnInfoDialog = ColumnInfoDialog(columnItem)
        ret = columnInfoDialog.exec_()
        if ret:
            self.onUpdateModel(False)

    def onUpdateModel(self, createNew=True):
        self.setupModel(createNew)

    def exec_(self):
        super(SettingsDialog, self).exec_()
        return self.path

    def setupJsonManager(self, path="config/Configuration.json"):
        self.path = path
        self.jsonManager = JsonManager()
        self.jsonManager.read(path)
        self.jsonManager.parse()
        if not self.jsonManager.validate():
            logging.error('Конфигурационный файл сломан')
            return

    def setupModel(self, createNew=True):
        self.columns = Columns.getInstance(self.jsonManager.jsonObject, createNew)
        self.model = QStandardItemModel()
        self.model.setVerticalHeaderItem(0, QStandardItem('name'))
        self.model.setVerticalHeaderItem(1, QStandardItem('type'))
        self.model.setVerticalHeaderItem(2, QStandardItem('generationType'))

        for columnIndex, key in enumerate(self.jsonManager.jsonObject.keys()):
            if 'count' == key:
                self.setUpRowCount()

            if 'name' == key:
                self.setUpTableName()

        for columnIndex, columnItem in enumerate(self.columns.columns):
            itemName = QStandardItem()
            itemName.setText(columnItem.name())
            itemName.setData(columnItem.Uuid(), 404)
            self.model.setItem(0, columnIndex, itemName)

            itemType = QStandardItem()
            itemType.setText(columnItem.type())
            itemType.setData(columnItem.Uuid(), 404)
            self.model.setItem(1, columnIndex, itemType)

            itemGenerationType = QStandardItem()
            itemGenerationType.setText(columnItem.generationType())
            itemGenerationType.setData(columnItem.Uuid(), 404)
            self.model.setItem(2, columnIndex, itemGenerationType)

        self.model.itemChanged.connect(self.onItemChanged)
        self.configView.setModel(self.model)

    def setUpRowCount(self):
        object = self.jsonManager.jsonObject
        countFromJson = object['count'].toInt()
        self.rowCount.setValue(countFromJson)

    def setUpTableName(self):
        object = self.jsonManager.jsonObject
        tableNameFromJson = object['name'].toString()
        self.tableName.setText(tableNameFromJson)

    def onLoadSettings(self):
        logging.info("Загрузка конфигурационного файла из настроек")
        fileName, _ = QFileDialog.getOpenFileName(self,
                                               "Окрыть конфигурацию", "", "Config Files (*.json)")
        if not fileName:
            return

        self.setupJsonManager(fileName)
        self.setupModel()

    def onSaveSettings(self):
        logging.info("Сохранение конфигурационного файла из настроек")
        json = JsonManager.createJson(self.columns.columns, self.tableName.text(), int(self.rowCount.text()))
        JsonManager.save(json, self.path)

    def onItemChanged(self, item: QStandardItem):
        rowIndex = item.row()
        columnId = item.data(404)
        columnItem = self.findColumnItem(columnId)
        if 0 == rowIndex:
            columnItem.setName(item.text())

        if 1 == rowIndex:
            columnItem.setType(item.text())

        if 2 == rowIndex:
            columnItem.setGenerationType(item.text())

    def findColumnItem(self, uuid):
        for columnItem in self.columns.columns:
            if columnItem.Uuid() == uuid:
                return columnItem

        return None
