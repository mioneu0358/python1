# Human 클래스 만들기
# 객체 생성시 이름, 나이, 직업 할당하기
# introduce(): 안녕하세요 제 이름은 00이고, 나이는 00살이며, 직업은 00입니다. 출력하기
class Human:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job
    def introduce(self):
        print(f"안녕하세요. 제 이름은 {self.name}이고, 나이는 {self.age}이며, 직업은 {self.job}입니다.")

    def __repr__(self):
        return f"{self.name}선생님"

# Student 클래스 만들기
# 객체 생성시 이름, 나이, 직업, 몇반 할당하기
# set_grade(): 국어, 영어, 수학 점수 할당하기
# get_average(): 국어, 영어, 수학 점수로 평균 구하기
class Studnet(Human):
    def set_grade(self,kor,eng,math):
        self.scores = list(map(int,[kor,eng,math]))
    def get_average(self):
        return sum(self.scores) / len(self.scores)
    def __repr__(self):
        return f"{self.name}학생"
# Teacher 클래스 만들기
# 객체 생성시 이름, 나이, 직업 몇반 할당하기
# introduce(): 안녕하세요 제 이름은 00이고, 나이는 00살이며 0반 담임선생님 겸 00선생님입니다. 출력하기

class Teacher(Human):
    def __init__(self, name,age,job,grade,cls_num):
        super().__init__(name,age,job)
        self.grade = grade
        self.cls_num = cls_num
    def introduce(self):
        print(f"안녕하세요. 제 이름은 {self.name}이고, 나이는 {self.age}이며, {self.cls_num}반 담임선생님 겸 {self.job}입니다.")


# School 클래스 만들기
# 객체 생성시 1,2,3학년별로 1반~3반을 가진다.
# set_info(): Human_info.txt를 읽어와서 학생객체 또는 선생객체 만들기
# 학생 정보는 이름 나이 반 국어점수 영어점수 수학점수로 이루어져 있고, 선생정보는 이름 나이 반 담당교과로 이루어져 있다.
# 각 객체의 내용을 가지고  해당하는 반에 할당하기
# show_class_avg(): 1,2,3학년 별로 각 반의 평균 점수와 등수를 등수 순서대로 보여주기
#                   1학년: 0반 00점, 0반 00점, 0반 00점
#                   2학년: 0반 00점, 0반 00점, 0반 00점
#                   3학년: 0반 00점, 0반 00점, 0반 00점

class School:
    def __init__(self):
        self.school_info = {
            '1학년': {'1반': {'teacher': '', 'std_info': []}, '2반': {'teacher': '', 'std_info': []}, '3반': {'teacher': '', 'std_info': []}},
            '2학년': {'1반': {'teacher': '', 'std_info': []}, '2반': {'teacher': '', 'std_info': []}, '3반': {'teacher': '', 'std_info': []}},
            '3학년': {'1반': {'teacher': '', 'std_info': []}, '2반': {'teacher': '', 'std_info': []}, '3반': {'teacher': '', 'std_info': []}}
        }
    def set_info(self):
        with open('Human_info.txt', 'r',encoding='utf8') as file:
            for line in file.readlines():
                info = line.split()
                if len(info) == 5:
                    name,age,grade,cls_num,job = info
                    t = Teacher(name,age,job,grade,cls_num)
                    self.school_info[f"{grade}학년"][f"{cls_num}반"]['teacher'] = t
                else:
                    name,age,job,cls_num,kor,eng,math = line.split()
                    std = Studnet(name,age,job)
                    std.set_grade(kor,eng,math)
                    std_grade = int(age) - 16
                    self.school_info[f"{std_grade}학년"][f"{cls_num}반"]['std_info'].append(std)
        print(self.school_info)
    def show_class_avg(self):
        result = {}
        for grade, all_class in self.school_info.items():
            result[grade] = {}
            for cls_num, cls_info in all_class.items():
                cls_avg = 0
                for std in cls_info['std_info']:
                    cls_avg += std.get_average()
                cls_avg /= len(cls_info['std_info'])
                result[grade][cls_num] = round(cls_avg,2)
        for grade in result:
            print(f"{grade} 반 평균 성적")

myschool = School()
myschool.set_info()
myschool.show_class_avg()


# Human_info.txt
# 김민준 17 학생 1 87 92 75
# 이서연 17 학생 1 78 85 90
# 박지훈 17 학생 1 92 74 88
# 최예린 17 학생 1 83 91 65
# 정우성 17 학생 1 80 72 98
# 박정수 42 1 1 국어선생님
# 한지민 17 학생 2 95 89 76
# 유재석 17 학생 2 74 80 85
# 송혜교 17 학생 2 86 95 79
# 강동원 17 학생 2 77 60 91
# 배수지 17 학생 2 94 77 68
# 이민재 39 1 2 영어선생님
# 차은우 17 학생 3 89 83 70
# 문채원 17 학생 3 75 68 88
# 신세경 17 학생 3 81 79 92
# 이병헌 17 학생 3 96 90 85
# 고소영 17 학생 3 85 71 93
# 김서윤 45 1 3 수학선생님
# 정해인 18 학생 1 78 87 67
# 수지현 18 학생 1 90 81 75
# 이다희 18 학생 1 87 79 88
# 정찬우 18 학생 1 91 85 80
# 최민호 18 학생 1 88 72 89
# 정상우 41 2 1 영어선생님
# 장동건 18 학생 2 92 77 84
# 강소라 18 학생 2 81 70 91
# 이동욱 18 학생 2 79 83 76
# 이정재 18 학생 2 97 94 85
# 손예진 18 학생 2 86 90 78
# 최다연 38 2 2 국어선생님
# 김태희 18 학생 3 84 75 92
# 김우빈 18 학생 3 89 68 80
# 이나영 18 학생 3 75 84 95
# 송중기 18 학생 3 90 78 88
# 전지현 18 학생 3 93 91 79
# 윤소민 46 2 3 수학선생님
# 이도현 19 학생 1 85 77 90
# 배유진 19 학생 1 76 85 87
# 오승민 19 학생 1 92 78 79
# 권지수 19 학생 1 81 92 84
# 최서연 19 학생 1 90 83 76
# 강지훈 37 3 1 수학선생님
# 한승우 19 학생 2 94 82 70
# 장지민 19 학생 2 85 74 91
# 노지훈 19 학생 2 79 90 87
# 문서영 19 학생 2 80 73 92
# 박소현 19 학생 2 91 89 77
# 배민경 43 3 2 국어선생님
# 이윤호 19 학생 3 88 80 85
# 최진호 19 학생 3 83 71 90
# 서하은 19 학생 3 76 89 84
# 조민수 19 학생 3 92 87 78
# 신예빈 19 학생 3 84 72 91
# 이상호 40 3 3 영어선생님
