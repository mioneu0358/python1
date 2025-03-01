# 학생과 선생님의 정보가 들어있는 text file human_info.txt가 주어졌을 때, 이를 학교 클래스에 저장하고, 각 학년별 반 평균들을 출력하는 함수를 작성하시오.
#
# Human class : 이름, 나이, 직업을 전달받은 사람 객체,
# introduce(): "안녕하세요. 저는 00살 00이라고 합니다. 제 직업은 00입니다." 를 출력하는 함수
# Student class: 이름, 나이, 직업을 전달받는 학생 객체
# set_scores(kor, eng, math):  국어, 영어 수학 점수를 전달받아, 객체의 속성값으로 할당하는 함수
# 학생객체는 출력 시 '000학생'이라고 출력되도록한다.
# Teacher class: 이름, 나이, 직업, 학년, 반을 전달받는 선생님 객체
# # introduce(): "안녕하세요. 저는 00학년 00반 담임선생님 000입니다. 제 나이는 00살이고, 담당과목은 00입니다.
# # 선생님 객체는 출력 시 '000선생님'이라고 출력되도록한다.
# set_info(file_name): 넘겨 받은 file_name에 들어있는 학생과 선생님 정보를 읽고, 객체의 속성값으로 할당하는 함수
# #                      학생은 이름 나이 직업 반 국어점수 영어점수 수학점수 형태로 구성되어있고,
# #                      선생님은 이름 나이 담당학년 담당반 직업으로 구성되어있다.
# #                      편의상 학년과 반은 각각 3개씩 있다고 가정한다.
# show_average(): 가지고 있는 학생 정보를 활용해서 각 학년 별 반 평균을 출력하는 함수, 각 반의 순서는 평균 성적이 높은 순으로 출력한다.
#         출력형태: 1학년 반 평균
#                  0반 90점, 0반 80점, 0반 70점
#                  2학년 반 평균
#                  0반 00점, 0반 00점, 0반 00점
#                  3학년 반 평균
#                  0반 00점, 0반 00점, 0반 00점
#

import os
class Human:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

    def introduce(self):
        print(f"안녕하세요. 저는 {self.age}살 {self.name}이라고 합니다. 제 직업은 {self.job}입니다.")



class Student(Human):
    def set_scores(self,kor,eng,math):
        self.scores = list(map(int,[kor,eng,math]))
    def __repr__(self):
        return f"{self.name}학생"

class Teacher(Human):
    def __int__(self,name,age,job,grade,class_):
        super().__init__(name,age,job)
        self.grade = grade
        self.class_ = class_
    def introduce(self):
        print(f"안녕하세요. 저는 {self.grade}학년 {self.class_}반 담임선생님 {self.name}입니다. 제 나이는 {self.age}이고, 담당과목은 {self.job}입니다.")
    def __repr__(self):
        return f"{self.name}선생님"
# School class: 학교객체
class School:
    def __init__(self):
        self.teachers_info = {}
        self.students_info = {}
        for grade in range(1,4):
            t = {}
            s = {}
            for class_ in range(1,4):
                t[class_] = ""
                s[class_] = []
            self.teachers_info[grade] = t
            self.students_info[grade] = s

    def set_info(self,file_name):
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"{file_name}을 찾을 수 없습니다.")
        with open(file_name, "r", encoding='utf8') as file:
            for line in file.readlines():
                line = line.split()
                if len(line) == 7:
                    name,age,job,class_,kor,eng,math = line
                    s = Student(name,age,job)
                    s.set_scores(kor,eng,math)
                    self.students_info[int(age) - 16][int(class_)].append(s)
                else:
                    name, age, grade,class_,job = line
                    t = Teacher(name,age,job)
                    self.teachers_info[int(grade)][int(class_)] = t




    def show_info(self):
        # 1학년 정보
        # 1반 담임선생님: 000선생님, 학생들: [000학생, 000학생, 000학생...], 2반 담임선생님: 000선생님, 학생들: [000학생, 000학생...], ....
        # ...
        for grade in range(1,4):
            print(f"{grade}학년 정보")
            for class_ in range(1,4):
                print(f"{class_}반: 담임선생님: {self.teachers_info[grade][class_]}, 학생들: {self.students_info[grade][class_]}")
    def show_average(self):
        for grade in range(1,4):
            print(f"{grade}학년 반별 평균")
            class_avgs = []
            for class_ in range(1,4):
                total = 0
                students = self.students_info[grade][class_]
                for std in students:
                    total += sum(std.scores)/ len(std.scores)
                class_avgs.append([class_,total/len(students)])
            class_avgs.sort(reverse=True,key=lambda x: x[1])
            for c_num, avg in class_avgs:
                print(f"{c_num}반: {round(avg,2)}점", end='  ')
            print()




A_school = School()
A_school.set_info('human_info.txt')
A_school.show_info()
print()
A_school.show_average()


# human_info.txt

# 김민준 17 학생 1 87 92 75
# 이서연 17 학생 1 78 85 90
# 박지훈 18 학생 1 92 74 88
# 최예린 17 학생 1 83 91 65
# 정우성 18 학생 1 80 72 98
# 박정수 42 1 1 국어선생님
# 한지민 18 학생 2 95 89 76
# 유재석 17 학생 2 74 80 85
# 송혜교 18 학생 2 86 95 79
# 강동원 17 학생 2 77 60 91
# 배수지 18 학생 2 94 77 68
# 이민재 39 1 2 영어선생님
# 차은우 18 학생 3 89 83 70
# 문채원 17 학생 3 75 68 88
# 신세경 18 학생 3 81 79 92
# 이병헌 17 학생 3 96 90 85
# 고소영 18 학생 3 85 71 93
# 김서윤 45 1 3 수학선생님
# 정해인 18 학생 1 78 87 67
# 수지현 18 학생 1 90 81 75
# 이다희 17 학생 1 87 79 88
# 정찬우 18 학생 1 91 85 80
# 최민호 17 학생 1 88 72 89
# 정상우 41 2 1 영어선생님
# 장동건 17 학생 2 92 77 84
# 강소라 18 학생 2 81 70 91
# 이동욱 17 학생 2 79 83 76
# 이정재 18 학생 2 97 94 85
# 손예진 17 학생 2 86 90 78
# 최다연 38 2 2 국어선생님
# 김태희 18 학생 3 84 75 92
# 김우빈 17 학생 3 89 68 80
# 이나영 18 학생 3 75 84 95
# 송중기 17 학생 3 90 78 88
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

