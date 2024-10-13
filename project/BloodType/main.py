class Human:
    def __init__(self, bloodtype):
        self.BloodType = bloodtype

class Parent(Human):
    pass

class Child(Human):
    def __init__(self,bloodtype,DAD,MOM):
        super().__init__(bloodtype)
        self.parent = [DAD,MOM]
    def bloodTypeCheck(self):
        Dad,Mom = self.parent
        BloodTypes = {'A': ['AA', 'AO'], 'B': ['BB', 'BO'], 'O': ['OO'], 'AB': ['AB']}

        possible = set()
        for DD in BloodTypes[Dad.BloodType]:  # 'AA','AO'
            for MM in BloodTypes[Mom.BloodType]:  # BB','BO'
                for D in DD:
                    for M in MM:
                        possible.add((D, M))
        print(possible)
        possible = list(map(lambda x: ''.join(sorted(x)), possible))
        print(possible)
        BloodType  = set()
        for pos in possible:
            for key,value in BloodTypes.items():
                if pos in value:
                    BloodType.add(key)
        print(BloodType)
        if self.BloodType in BloodType:
            return True
        else:
            return False


father = Parent(input("아버지의 혈액형을 입력하시오: "))
mother = Parent(input("어머니의 혈액형을 입력하시오: "))

I = Child(input("나의 혈액형을 입력하시오: "),father,mother)
print(I.bloodTypeCheck())
