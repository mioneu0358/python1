

class Human:
    # 혈액형의 유전 정보를 딕셔너리로 정의
    ABO_bloodType = {
        'A': {'AA', 'AO'},
        'B': {'BB', 'BO'},
        'O': {'OO'},
        'AB': {'AB'},
        '': None
    }

    def __init__(self,name, bloodtype=None):
        # 혈액형 정보를 저장
        self.name = name
        self.bloodType = bloodtype
        self.Dad = None
        self.Mom = None


    def set_parent(self, dad=None, mom=None):
        """부모 객체를 설정"""
        self.Dad = dad
        self.Mom = mom

    def get_my_bloodType(self):
        # 부모의 혈액형 가져오기
        Dad_bloodType = self.Dad.get_my_bloodType() if self.Dad else None
        print(f"{self.name}의 Dad_bloodType: {Dad_bloodType}")
        Mom_bloodType = self.Mom.get_my_bloodType() if self.Mom else None
        print(f"{self.name}의 Mom_bloodType: {Mom_bloodType}")

        # 본인의 혈액형이 이미 설정되어 있으면 반환
        if self.bloodType:
            # 특수 혈액형 처리
            if self.bloodType == 'O' and (Dad_bloodType == 'AB' and Mom_bloodType == 'O' or Dad_bloodType == 'O' and Mom_bloodType == 'AB'):
                return "Cis-AB"
            elif Dad_bloodType == Mom_bloodType == {'O'} and self.bloodType in ['A','B']:
                return '봄베이 O'
            return self.bloodType


        # 부모님중 한명이라도 혈액형 정보가 없는 경우
        if Dad_bloodType is None or Mom_bloodType is None:
            return None
        possible_bloodtypes = set()
        # 두분 다 정해져 있는 경우
        if type(Dad_bloodType) == type(Mom_bloodType) == str:
            for dad in self.ABO_bloodType[Dad_bloodType]:
                for mom in self.ABO_bloodType[Mom_bloodType]:
                    for gene_dad in dad:
                        for gene_mom in mom:
                            possible_bloodtypes.add(''.join(sorted((gene_dad, gene_mom))))

        elif type(Dad_bloodType) == type(Mom_bloodType) == list:
            for dad in Dad_bloodType:
                for mom in Mom_bloodType:
                    for gene_dad in dad:
                        for gene_mom in mom:
                            possible_bloodtypes.add(''.join(sorted((gene_dad, gene_mom))))

        # 어머니 정해져 있는 경우
        elif type(Dad_bloodType) == list :
            for dad in Dad_bloodType:
                for mom in self.ABO_bloodType[Mom_bloodType]:
                    for gene_dad in dad:
                        for gene_mom in mom:
                            possible_bloodtypes.add(''.join(sorted((gene_dad, gene_mom))))

        else:
            for mom in Mom_bloodType:
                for dad in self.ABO_bloodType[Dad_bloodType]:
                    for gene_mom in mom:
                        for gene_dad in dad:
                            possible_bloodtypes.add(''.join(sorted((gene_dad, gene_mom))))
        return sorted(possible_bloodtypes)
