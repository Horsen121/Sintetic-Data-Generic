from ui.PersistentDialog import *
from managers.ColumnsManager import Columns


class ColumnInfoDialog(PersistentDialog):
    def __init__(self, columnItem):
        super().__init__()
        self.columnItem = columnItem
        self.setupUi()
        self.setupModel()
        self.model.itemChanged.connect(self.onItemChanged)

    def setupUi(self):
        mainLayout = QVBoxLayout()
        self.dataView = QTableView()
        self.dataView.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.model = QStandardItemModel()
        self.model.setVerticalHeaderItem(0, QStandardItem('name'))
        self.model.setVerticalHeaderItem(1, QStandardItem('type'))
        self.model.setVerticalHeaderItem(2, QStandardItem('generationType'))
        self.dataView.horizontalHeader().hide()
        self.dataView.horizontalHeader().setStretchLastSection(True)
        self.dataView.setModel(self.model)

        mainLayout.addWidget(self.dataView)
        self.setLayout(mainLayout)

    def contextMenuEvent(self, event):
        hheader, vheader = self.dataView.horizontalHeader(), self.dataView.verticalHeader()
        position = event.globalPos()
        row = vheader.logicalIndexAt(vheader.mapFromGlobal(position))
        column = hheader.logicalIndexAt(hheader.mapFromGlobal(position))

        menu = QMenu(self)
        if row < 0 or column < 0:
            createColumnAction = menu.addAction("Добавить свойство")
            createColumnAction.triggered.connect(lambda:
                                                 self.onCreateProperty()
                                                 )
        else:

            removePropertyAction = menu.addAction("Удалить свойство")
            removePropertyAction.triggered.connect(lambda:
                                                   self.onRemoveProperty()
                                                   )

        menu.exec_(position)

    def onRemoveProperty(self):
        logging.info("trash")

    def onCreateProperty(self):
        logging.info("trash")

    def setupModel(self):
        columnIndex = 0
        row = 0
        itemName = QStandardItem()
        itemName.setText(self.columnItem.name())
        itemName.setData(self.columnItem.Uuid(), 404)
        self.model.setItem(row, columnIndex, itemName)
        row += 1

        itemType = QStandardItem()
        itemType.setText(self.columnItem.type())
        itemType.setData(self.columnItem.Uuid(), 404)
        self.model.setItem(row, columnIndex, itemType)
        row += 1

        itemGenerationType = QStandardItem()
        itemGenerationType.setText(self.columnItem.generationType())
        itemGenerationType.setData(self.columnItem.Uuid(), 404)
        self.model.setItem(row, columnIndex, itemGenerationType)
        if self.columnItem.data() is None:
            return

        for key, value in self.columnItem.data().items():
            item = QStandardItem()
            row += 1
            if value.isArray():
                value = value.toArray()
                pyValue = []
                for el in value:
                    pyValue.append(el.toString())

                value = ','.join(pyValue)
            else:
                value = value.toString()

            item.setText(value)
            self.model.setItem(row, columnIndex, item)
            self.model.setVerticalHeaderItem(row, QStandardItem(key))

    def onItemChanged(self, item: QStandardItem):
        rowIndex = item.row()
        columns = Columns.getInstance()
        itemForChange = None
        needToAppend = False
        changed = False
        for columnItem in columns.columns:
            if columnItem.Uuid() == self.columnItem.Uuid():
                itemForChange = columnItem
                break

        if itemForChange is None:
            needToAppend = True
            itemForChange = self.columnItem

        if 0 == rowIndex:
            itemForChange.setName(item.text())
            changed = True

        if 1 == rowIndex:
            itemForChange.setType(item.text())
            changed = True

        if 2 == rowIndex:
            itemForChange.setGenerationType(item.text())
            changed = True

        if not changed:
            itemData = itemForChange.data()
            itemData[self.model.verticalHeaderItem(rowIndex).text()] = QJsonValue(item.text())
            itemForChange.setData(itemData)

        if needToAppend:
            columns.columns.append(itemForChange)

    def exec_(self):
        super(ColumnInfoDialog, self).exec_()
        return True
