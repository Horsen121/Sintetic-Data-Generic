from PyQt5.QtCore import QFile, QJsonDocument, QJsonParseError, QByteArray
from PyQt5.QtGui import QStandardItemModel
import logging
import os


class JsonManager:
    def __init__(self):
        self.data = None

    def read(self, path):
        file = QFile(os.path.abspath(path))
        file.open(QFile.ReadOnly)
        if file.isOpen() == 1:
            self.data = file.readAll()
        else:
            logging.error("Не удалось загрузить файл конфигурации")

        file.close()

    def parse(self):
        if self.data is None:
            return

        error = QJsonParseError()
        json = QJsonDocument.fromJson(self.data, error)
        self.jsonObject = json.object()

    def validate(self) -> bool:
        isCountExist = 'count' in self.jsonObject.keys()
        isNameExist = 'name' in self.jsonObject.keys()

        return isCountExist and isNameExist

    @staticmethod
    def createJson(columns, tableName, rowCount):
        data = QByteArray()
        jsonDocument = QJsonDocument()
        json = jsonDocument.fromJson(data).object()
        json["name"] = tableName
        json["count"] = rowCount
        for columnItem in columns:
            columnItemJson = QJsonDocument.fromJson(data).object()
            columnItemJson["name"] = columnItem.name()
            columnItemJson["type"] = columnItem.type()
            columnItemJson["typeGeneration"] = columnItem.generationType()
            if columnItem.data() is not None:
                for key, value in columnItem.data().items():
                    columnItemJson[key] = value

            json[str(columnItem.jsonColumnName())] = columnItemJson

        jsonDocument.setObject(json)

        return jsonDocument

    @staticmethod
    def save(json, fileName='Configuration.json'):
        jsonFile = QFile(fileName)
        jsonFile.open(QFile.WriteOnly)
        jsonFile.write(json.toJson())
        jsonFile.close()
        logging.info("Сохранение прошло успешно!")
