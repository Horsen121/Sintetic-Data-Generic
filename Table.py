from dataclasses import dataclass
import time

@dataclass
class Table:
    name = "table"
    count = 10000
    Columns = {
        #0 : {
        #    "name" : "Birthday",
        #    "typeGeneration" : "Data" 
        #    },
        #1 : {
        #    "name" : "Name",
        #    "typeGeneration" : "Strings"
        #    },
        #2 : {
        #    "name" : "Email",
        #    "typeGeneration" : "Email"
        #    }
    }
    
    def __getitem__(self, string):
        return self.string

dataDefault = {
    "count" : 10000,
    "methods" : ("Numbers","Strings","Collection","Masks","Data","Timestamp","Join","Gender","FIO","Lastname","Name","Patronymic","Email","Phone"),
    "type" : "int",
    "num_range1" : 0,
    "num_range2" : 1000,
    "symbols" : ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"," "],
    "strlen" : 50,
    "date_firstBorder" : "20000101",
    "date_secondBorder" : "20220101",
    "timestamp_firstBorder" : 0,
    "timestamp_secondBorder" : int(time.time()),
    "list" : {"1":0,"2":0,"3":0,"4":0,"5":0},
    "mask" : "2#.##.2042"
}