import json, csv
import os
import Table
from Generator import Generator
from MimesisGenerator import MimesisGenerator
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('DataHack').getOrCreate()


class Configurate():

    tableName = ""
    count = 0

    @staticmethod
    def LoadFromJson(path="config/Configuration.json"):
        with open(os.path.abspath(path), encoding='UTF-8') as file:
            dataJ = json.load(file)     
        
        items = list(dataJ.items())
        listParametrs = []
        typeGenerations = []

        for i in range(0, len(dataJ)):
            if (list(items[i]))[0] == "name":
                Configurate.tableName = (list(items[i]))[1]
                continue
            elif (list(items[i]))[0] == "count":
                Configurate.count = int((list(items[i]))[1])
                continue

            columnInfo = (list(items[i]))[1]
            listParametrs.append(columnInfo)
            typeGenerations.append(dict(columnInfo).get("typeGeneration"))

        if Configurate.tableName == "":
            Configurate.tableName = Table.Table.name
        if Configurate.count == 0:
            Configurate.count = Table.Table.count


        return Configurate.CreatingData(typeGenerations,listParametrs,Configurate.count)

    def CreatingData(methods,parametrs,count):
        columns = []
        dictionary = {}
        for i in range(0, len(parametrs)):
             dictionary[i] = dict(parametrs[i])

        defaultColumnsNames = Configurate.GetColumnsNames(dict(Table.Table.Columns))
        jsonColumnsNames = Configurate.GetColumnsNames(dictionary)
        notJsonColumnsNames = [el for el in defaultColumnsNames if el not in jsonColumnsNames]


        tmp = dict(Table.Table.Columns)
        fields = []
        for i in range(0, len(tmp)):
            t = tmp.get(i)
            fields.append(t.get("typeGeneration"))

        if(len(methods) == 0):
            columns += (Configurate.GenerateFromDefaults(fields))
        elif(len(methods) == len(fields) and Configurate.IsTheSameNames(defaultColumnsNames, jsonColumnsNames)):
            columns += (Configurate.GenerateFromJson(parametrs, count))
        else:
            columns += (Configurate.GenerateFromJson(parametrs, count))
            if notJsonColumnsNames != None:
                list = []
                for i in range(0, len(tmp)):
                    t = tmp.get(i)
                    if t.get("name") in notJsonColumnsNames:
                        list.append(t.get("typeGeneration"))
                columns += (Configurate.GenerateFromDefaults(list))

            
        return Configurate.DataOutput(count, columns, jsonColumnsNames + notJsonColumnsNames)

    def GenerateFromDefaults(fields):
        columns = []
        generator = Generator()
        MimGen = MimesisGenerator()
        dataD = Table.dataDefault
        count = Table.Table.count

        for i in fields:
                if i == "Numbers": 
                    column = generator.Numbers(dataD.get("type"),dataD.get("num_range1"),dataD.get("num_range2"),dataD.get("count"))
                elif i == "Strings":
                    column = generator.Strings(dataD.get("symbols"),dataD.get("strlen"),count)
                elif i == "Collection": 
                    column = generator.Collection(dataD.get("list"),count)
                elif i == "Masks": 
                    column = generator.Masks(dataD.get("type"),dataD.get("mask"),count)
                elif i == "Data": 
                    column = generator.Data(dataD.get("date_firstBorder"),dataD.get("date_secondBorder"),count)
                elif i == "Timestamp": 
                    column = generator.Timestamp(dataD.get("timestamp_firstBorder"),dataD.get("timestamp_secondBorder"),count)
                elif i == "Gender":
                    column = MimGen.Gender(count)
                elif i == "FIO":
                    column = MimGen.FIO(count)
                elif i == "Lastname":
                    column = MimGen.Lastname(count)
                elif i == "Name":
                    column = MimGen.Name(count)
                elif i == "Patronymic":
                    column = MimGen.Patronymic(count)
                elif i == "Email":
                    column = MimGen.Email(count)
                elif i == "Phone":
                    column = MimGen.Phone(count)
                columns.append(column)
        return columns
    
    def GenerateFromJson(parametrs, count):
        columns = []
        generator = Generator()
        MimGen = MimesisGenerator()
        dataD = Table.dataDefault

        for j in parametrs:
                if j.get("typeGeneration") == "Numbers" and "range" in j:
                    ran = str(j.get("range")).split("-")
                    column = generator.Numbers(j.get("type"),int(ran[0]),int(ran[1]),count)
                elif j.get("typeGeneration") == "Numbers": 
                    column = generator.Numbers(j.get("type"),dataD.get("num_range1"),dataD.get("num_range2"),dataD.get("count"))
                
                if j.get("typeGeneration") == "Strings" and "symbols" in j:
                    if(j.get("length")): length = int(j.get("length"))
                    else: length = dataD.get("strlen")
                    column = generator.Strings(j.get("symbols"),length,count)
                elif j.get("typeGeneration") == "Strings" and "length" in j: 
                    column = generator.Strings(dataD.get("symbols"),j.get("length"),count)
                elif j.get("typeGeneration") == "Strings":
                    column = generator.Strings(dataD.get("symbols"),dataD.get("strlen"),count)

                if j.get("typeGeneration") == "Collection" and "list" in j:
                    dict = {}
                    list = j.get("list")
                    if(type(list) == type(columns)):
                        for i in range(len(list)):
                            dict[list[i]] = 0
                        column = generator.Collection(dict,count)
                    else: column = generator.Collection(list,count)
                elif j.get("typeGeneration") == "Collection": 
                    column = generator.Collection(dataD.get("list"),count)

                if j.get("typeGeneration") == "Masks" and "mask" in j and "typeMask" in j:
                    column = generator.Masks(j.get("typeMask"),j.get("mask"),count)
                elif j.get("typeGeneration") == "Masks" and "typeMask" in j:
                    column = generator.Masks(j.get("typeMask"),dataD.get("mask"),count)
                elif j.get("typeGeneration") == "Masks" and "mask" in j:
                    column = generator.Masks(dataD.get("typeMask"),j.get("mask"),count)
                elif j.get("typeGeneration") == "Masks": 
                    column = generator.Masks(dataD.get("type"),dataD.get("mask"),count)

                if j.get("typeGeneration") == "Data" and "firstBorder" in j and "secondBorder" in j:
                    column = generator.Data(j.get("firstBorder"),j.get("secondBorder"),count)
                elif j.get("typeGeneration") == "Data" and "firstBorder" in j: 
                    column = generator.Data(j.get("firstBorder"),dataD.get("date_secondBorder"),count)
                elif j.get("typeGeneration") == "Data": 
                    column = generator.Data(dataD.get("date_firstBorder"),dataD.get("date_secondBorder"),count)

                if j.get("typeGeneration") == "Timestamp" and "firstBorder" in j and "secondBorder" in j: 
                    column = generator.Timestamp(j.get("firstBorder"),j.get("secondBorder"),count)
                elif j.get("typeGeneration") == "Timestamp" and "secondBorder" in j: 
                    column = generator.Timestamp(j.get("secondBorder"),count)
                elif j.get("typeGeneration") == "Timestamp": 
                    column = generator.Timestamp(dataD.get("timestamp_firstBorder"),dataD.get("timestamp_secondBorder"),count)
                    
                if j.get("typeGeneration") == "Join" and "table" in j and "column" in j: #...default table?
                    table_name = j.get("table")
                    col = j.get("column")
                    column = generator.Join(Configurate.ColumnFromCSV(table_name, col),count)

                if j.get("typeGeneration") == "Gender":
                    column = MimGen.Gender(count)

                if j.get("typeGeneration") == "FIO":
                    column = MimGen.FIO(count)

                if j.get("typeGeneration") == "Lastname":
                    column = MimGen.Lastname(count)

                if j.get("typeGeneration") == "Name":
                    column = MimGen.Name(count)

                if j.get("typeGeneration") == "Patronymic":
                    column = MimGen.Patronymic(count)

                if j.get("typeGeneration") == "Email":
                    column = MimGen.Email(count)

                if j.get("typeGeneration") == "Phone":
                    column = MimGen.Phone(count)

                columns.append(column)
        return columns

    def IsTheSameNames(defaultNames:list, jsonNames:list):
        defaultNames.sort()
        jsonNames.sort()

        if jsonNames == defaultNames:
            return True
        else:
            return False

    def GetColumnsNames(parametrs:dict):
        columnsNames = []
        for i in range(0, len(parametrs)):
            t = parametrs.get(i)
            columnsNames.append(t.get("name"))
        return columnsNames

    @staticmethod
    def DataOutput(count, columns, columnsNames):
        data = []
        row = []

        for rowIdx in range(count):
            row = []
            for i in range(len(columns)):
                row.append(columns[i][rowIdx])

            data.append(row)

        Configurate.CreateDataFrame(columnsNames, data)
        return columnsNames, data

    @staticmethod
    def CreateDataFrame(columnsNames, data):
        #Прописать, чтобы одна  не удаляла другую, если уже такая существует
        name = f"csv\{Configurate.tableName}.csv"

        with open(name, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            file_writer.writerow(columnsNames)
            for i in range(0, len(data)):
                file_writer.writerow(data[i])
        
        df = spark.read.csv("csv\data.csv", sep=",", inferSchema=True)
        return df

    @staticmethod
    def getInfoFromCSV(path):
        tmp = []
        with open(os.path.abspath(path), encoding='UTF-8') as table:
            reader = csv.reader(table, delimiter=',')
            for row in reader:
                tmp.append(row)

        return tmp[0], tmp[1:]

    @staticmethod
    def ColumnFromCSV(table, column):
        
                    tmp = []
                    list = []
                    path = f"csv/{table}.csv"
                    with open(path, mode="r", encoding='utf-8') as tablee:
                        reader = csv.reader(tablee, delimiter=',')
                        for row in reader:
                            tmp.append(row)
                    for i in range(0, len(tmp)):
                        tr = tmp[i]
                        list.append(tr[column])
                    return list
                        
                    

        