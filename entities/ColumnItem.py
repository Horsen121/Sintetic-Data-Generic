import uuid


class ColumnItem:
    def __init__(self, jsonColumnName):
        super().__init__()
        self.__jsonColumnName = jsonColumnName
        self.__uuid = uuid.uuid4()
        self.__columnIndex = None
        self.__name = None
        self.__type = None
        self.__data = None
        self.__typeGeneration = None

    def jsonColumnName(self):
        return self.__jsonColumnName

    def setColumnIndex(self, columnIndex):
        self.__columnIndex = columnIndex

    def Uuid(self):
        return self.__uuid

    def columnIndex(self):
        return self.__columnIndex

    def setName(self, name):
        self.__name = name

    def setType(self, columnType):
        self.__type = columnType

    def type(self):
        return self.__type

    def name(self):
        return self.__name

    def setData(self, data):
        self.__data = data

    def data(self):
        return self.__data

    def setGenerationType(self, generationType):
        self.__typeGeneration = generationType

    def generationType(self):
        return self.__typeGeneration
