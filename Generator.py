import random
import time
import operator

class Generator():
    
    numberFunctions = 6

    def __init__(self):
        pass

    def Numbers(self,type,range1,range2,count):
        res = []
        if(type == 'int'):
            for i in range(0,count):
                res.append(random.randint(range1,range2))
        else:
            for i in range(0,count):
                res.append(random.uniform(range1,range2))
        return res

    def Strings(self,symb,length,count):
        res = []
        for i in range(0,count):
            tmp = ""
            for j in range(0,length):
                tmp += (random.choice(symb))
            res.append(tmp)
        return res 

    def Collection(self, data,count):
        res = []
        if(list(data.values())[0] == 0):
            values = list(data.keys())
            for i in range(0,count):
                res.append(random.choice(values))
        else:
            sorted_tuples = sorted(data.items(), key=operator.itemgetter(1))
            sorted_dict = {k: v for k, v in sorted_tuples}
            for i in range(len(sorted_dict)):
                len = count//10 * list(sorted_dict.values())[i]
                for i in range(0,len):
                    res.append(list(data.keys())[i-1])
        return res 

    def Join(self, data, count):
        res = []
        for i in range(0,count):
            res.append(random.choice(data))
        return res 

    def Masks(self,type,mask,count):
        res = []
        if(type == 'int'):
            num = [1,2,3,4,5,6,7,8,9,0]
            for i in range(0,count):
                tmp = ""
                for j in mask:
                    if(j == "#"):
                        tmp += (str(random.choice(num)))
                    else: tmp += j
                res.append(tmp)
        elif(type == "str"):
            symb = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"," "]
            for i in range(0,count):
                tmp = ""
                for j in mask:
                    if(j == "#"):
                        tmp += (random.choice(symb))
                    else: tmp += j
                res.append(tmp)
        elif isinstance(type, list):
            for i in range(0,count):
                tmp = ""
                for j in mask:
                    if(j == "#"):
                        tmp += (random.choice(type))
                    else: tmp += j
                res.append(tmp)
        return res 

    def Data(self, firstBorder:str, secondBorder:str, count:int):
        
        data = []
        fyear = int(firstBorder[0:4])
        fmonth = int(firstBorder[4:6])
        fday = int(firstBorder[6:8])
        syear = int(secondBorder[0:4])
        smonth = int(secondBorder[4:6])
        sday = int(secondBorder[6:8])
        
        for i in range(0, count):
            newYear = random.randint(fyear, syear)
            if fyear == syear:
                newMonth = random.randint(fmonth, smonth)
            else:
                newMonth = random.randint(1, 12)

            if fyear == syear and fmonth == smonth:
                newDay = random.randint(fday, sday)
            else:
                if newMonth in [1, 3, 5, 7, 8, 10, 12]:
                    newDay = random.randint(1, 31)
                elif newMonth in [4, 6, 9, 11]:
                    newDay = random.randint(1, 30)
                else:
                    newDay = random.randint(1, 28)
            
            data.append(str(newYear))
            if newMonth < 10:
                data[i] += "-0" + str(newMonth)
            else:
                data[i] += "-" + str(newMonth)
            if newDay < 10:
                data[i] += "-0" + str(newDay)
            else:
                data[i] += "-" + str(newDay)
                    
        return data

    def Timestamp(self, firstBorder, secondBorder, count:int):

        timestamp = []
        for i in range(0, count):
            ts = time.gmtime(random.randint(int(firstBorder), int(secondBorder)))
            timestamp.append(time.strftime("%Y-%m-%d", ts))

        return timestamp

    #def Timestamp(self, secondBorder, count:int):
    #    timestamp = []
    #    for i in range(0, count):
    #        ts = time.gmtime(random.randint(0, secondBorder))
    #        timestamp.append(time.strftime("%Y-%m-%d", ts))
    #    return timestamp