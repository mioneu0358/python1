from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QComboBox, QTextEdit
)
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt
import sys


class Human:
    """혈액형과 부모-자식 관계를 관리하는 클래스"""
    ABO_bloodType = {
        'A': {'AA', 'AO'},
        'B': {'BB', 'BO'},
        'O': {'OO'},
        'AB': {'AB'},
        '': None
    }

    def __init__(self, name, bloodtype=None):
        self.name = name
        self.bloodType = bloodtype
        self.Dad = None
        self.Mom = None

    def set_parent(self, dad=None, mom=None):
        """부모 객체를 설정"""
        self.Dad = dad
        self.Mom = mom

    def get_my_bloodType(self):
        """혈액형 추론 로직"""
        Dad_bloodType = self.Dad.get_my_bloodType() if self.Dad else None
        Mom_bloodType = self.Mom.get_my_bloodType() if self.Mom else None

        # 본인의 혈액형이 이미 설정되어 있으면 반환
        if self.bloodType:
            return self.bloodType

        if Dad_bloodType is None or Mom_bloodType is None:
            return None

        possible_bloodtypes = set()
        for dad_gene in Human.ABO_bloodType.get(Dad_bloodType, []):
            for mom_gene in Human.ABO_bloodType.get(Mom_bloodType, []):
                for gene_dad in dad_gene:
                    for gene_mom in mom_gene:
                        possible_bloodtypes.add(''.join(sorted((gene_dad, gene_mom))))
        return sorted(possible_bloodtypes)

class FamilyTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("가족 구성도 혈액형 추론")
        self.setGeometry(100, 100, 300, 600)
        self.setFixedSize(300, 600)

        # 초기 가족 구성원
        self.initial_members = ["아버지", "어머니", "나"]

        # 메인 위젯
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 메인 레이아웃
        grid_layout = QGridLayout(main_widget)

        # "가족구성원 선택" 라벨
        label_select_family = QLabel("가족구성원 선택")
        label_select_family.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_select_family, 0, 0, 1, 4)

        # 가족구성원 선택 콤보박스
        self.add_member_box = QComboBox()
        self.add_member_box.addItems(["형제", "자매", "할아버지", "할머니", "외할아버지", "외할머니"])
        grid_layout.addWidget(self.add_member_box, 1, 0, 1, 4)

        # 가족구성원 추가/삭제 버튼
        self.add_member_button = QPushButton("구성원 추가")
        self.add_member_button.clicked.connect(self.add_family_member)
        self.delete_member_button = QPushButton("구성원 삭제")
        self.delete_member_button.clicked.connect(self.delete_family_member)

        grid_layout.addWidget(self.add_member_button, 2, 0, 1, 2)
        grid_layout.addWidget(self.delete_member_button, 2, 2, 1, 2)

        # "가족구성원 및 혈액형" 라벨
        label_family_table = QLabel("가족구성원 및 혈액형")
        label_family_table.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_family_table, 3, 0, 1, 4)

        # 가족구성원 테이블
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["구성원", "혈액형"])
        grid_layout.addWidget(self.table, 4, 0, 1, 4)

        # "혈액형을 확인할 가족구성원 선택" 라벨
        label_check_bloodtype = QLabel("혈액형을 확인할 가족구성원 선택")
        label_check_bloodtype.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_check_bloodtype, 5, 0, 1, 4)

        # 가족구성원 선택 콤보박스 (혈액형 확인)
        self.select_member_box = QComboBox()
        self.select_member_box.addItems(self.initial_members)
        grid_layout.addWidget(self.select_member_box, 6, 0, 1, 4)

        # 혈액형 확인하기 버튼
        check_button = QPushButton("혈액형 확인하기")
        check_button.clicked.connect(self.check_bloodtype)
        grid_layout.addWidget(check_button, 7, 0, 1, 4)

        # "가능한 혈액형" 라벨
        label_result = QLabel("가능한 혈액형")
        label_result.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(label_result, 8, 0, 1, 4)

        # 결과 박스
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFixedHeight(80)  # 2줄 정도의 문자를 표시할 높이
        font = QFont()
        font.setPointSize(12)  # 폰트 크기 설정
        self.result_box.setFont(font)
        self.result_box.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.result_box, 9, 0, 1, 4)

        # 업데이트
        self.update_table()

    def update_table(self):
        """테이블을 초기화 및 업데이트"""
        self.table.setRowCount(len(self.initial_members))
        for row, name in enumerate(self.initial_members):
            bloodtype = "???"  # 초기 혈액형 값
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(bloodtype))

        # 선택 박스도 동기화
        self.select_member_box.clear()
        self.select_member_box.addItems(self.initial_members)

    def add_family_member(self):
        """가족 구성원을 추가"""
        member_name = self.add_member_box.currentText()
        if member_name in self.initial_members:
            return  # 이미 존재하는 구성원은 추가하지 않음

        self.initial_members.append(member_name)
        self.update_table()

    def delete_family_member(self):
        """가족 구성원을 삭제"""
        member_name = self.add_member_box.currentText()
        if member_name in self.initial_members:
            self.initial_members.remove(member_name)
            self.update_table()

    def check_bloodtype(self):

        self.relations = {  # 부모 관계 정의
            "나": ["아버지", "어머니"],
            "아버지": ["할아버지", "할머니"],
            "어머니": ["외할아버지", "외할머니"]
        }
        human_objects = {}
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text()
            bloodtype = self.table.item(row, 1).text()
            human_objects[name] = Human(name, bloodtype if bloodtype != "???" else None)

        for name, obj in human_objects.items():
            print(f"이름: {name}, 혈액형: {obj.bloodType}")


        # 부모 관계 설정
        for child, parents in self.relations.items():
            print(child,parents)
            if child in human_objects:
                dad = human_objects.get(parents[0])
                mom = human_objects.get(parents[1])
                human_objects[child].set_parent(dad, mom)
        print("관계 설정 끝")

        # 선택된 구성원의 혈액형 확인
        selected_name = self.select_member_box.currentText()
        if selected_name in human_objects:
            result = human_objects[selected_name].get_my_bloodType()
            if isinstance(result, list):
                self.result_box.setText(f"{', '.join(result)}")
            elif result:
                self.result_box.setText(f"혈액형: {result}")
            else:
                self.result_box.setText("혈액형을 추론할 수 없습니다.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FamilyTreeApp()
    window.show()
    sys.exit(app.exec_())