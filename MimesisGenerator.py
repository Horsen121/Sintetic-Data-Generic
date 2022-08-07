import random
from mimesis import Person
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender

class MimesisGenerator():
    numberFunctions = 7
    def __init__(self):
        pass
    p = Person('ru')
    sp = RussiaSpecProvider()
    m = Gender.MALE
    f = Gender.FEMALE

    def Gender(self,count):
        res = []
        for i in range(0,count):
            r = random.randint(0,1)
            if(r == 1): res.append(self.f)
            else: res.append(self.m)
        return res

    def FIO(self,count):
        res = []
        for i in range(0,count):
            r = random.randint(0,1)
            if(r == 1): gender = self.f
            else: gender = self.m
            res.append(self.p.last_name(gender) + ' ' + self.p.first_name(gender) + ' ' + self.sp.patronymic(gender))
        return res

    def Lastname(self,count):
        res = []
        for i in range(0,count):
            r = random.randint(0,1)
            if(r == 1): gender = self.f
            else: gender = self.m
            res.append(self.p.last_name(gender))
        return res

    def Name(self,count):
        res = []
        for i in range(0,count):
            r = random.randint(0,1)
            if(r == 1): gender = self.f
            else: gender = self.m
            res.append(self.p.first_name(gender))
        return res

    def Patronymic(self,count):
        res = []
        for i in range(0,count):
            r = random.randint(0,1)
            if(r == 1): gender = self.f
            else: gender = self.m
            res.append(self.sp.patronymic(gender))
        return res

    def Email(self,count):
        res = []
        for i in range(0,count):
            res.append(self.p.email())
        return res

    def Phone(self,count):
        res = []
        for i in range(0,count):
            res.append(self.p.telephone())
        return res#