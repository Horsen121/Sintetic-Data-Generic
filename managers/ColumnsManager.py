from entities.ColumnItem import ColumnItem


class Columns:
    __instance = None
    __jsonObject = None

    def __init__(self, jsonObject):
        self.__jsonObject = jsonObject
        self.columns = createColumns(jsonObject)

    @classmethod
    def getInstance(cls, jsonObject=None, createNew=False):
        if not cls.__instance or createNew:
            cls.__instance = Columns(jsonObject)
        return cls.__instance


def createColumns(jsonObject):
    columns = []
    for columnIndex, key in enumerate(jsonObject.keys()):
        if key in ['count', 'name']:
            continue

        columnItem = ColumnItem(key)
        columnItem.setColumnIndex(columnIndex)
        info = jsonObject[key].toObject()
        data = {}
        for rowIndex, key in enumerate(info.keys()):
            if 'name' == key:
                columnItem.setName(info[key].toString())
                continue

            if 'type' == key:
                columnItem.setType(info[key].toString())
                continue

            if 'typeGeneration' == key:
                columnItem.setGenerationType(info[key].toString())
                continue

            data[key] = info[key]

        columnItem.setData(data)
        columns.append(columnItem)

    return columns
