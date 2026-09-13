import sys, os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QDockWidget, QLabel, QLineEdit,
                               QTreeWidget, QTreeWidgetItem, QTableWidget, 
                               QTabWidget, QComboBox, QSpinBox, QPushButton, 
                               QStatusBar, QDialog, QGroupBox, QHeaderView, 
                               QToolBar, QMenuBar, QColorDialog,QCheckBox,QMessageBox,
                               QSplitter, QFrame, QGridLayout, QTableWidgetItem)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QColor
from kiwoom_api import KiwoomRestAPI
from dotenv import load_dotenv, set_key

class LoginDialog(QDialog):
    def __init__(self, api_handler):
        super().__init__()
        self.api = api_handler
        self.setWindowTitle("HTS API 로그인")
        self.resize(350, 200)
        
        layout = QVBoxLayout(self)
        
        # APP KEY 입력란
        layout.addWidget(QLabel("APP KEY:"))
        self.key_input = QLineEdit()
        layout.addWidget(self.key_input)
        
        # APP SECRET 입력란 (비밀번호 마스킹 처리)
        layout.addWidget(QLabel("APP SECRET:"))
        self.secret_input = QLineEdit()
        self.secret_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.secret_input)
        
        # Key 기억하기 체크박스
        self.remember_cb = QCheckBox("Key 기억하기")
        layout.addWidget(self.remember_cb)
        
        # 로그인 버튼
        self.login_btn = QPushButton("로그인 (토큰 발급)")
        self.login_btn.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_btn)
        
        # 창이 켜질 때 기존 .env 파일이 있다면 불러오기
        self.load_env()

    def load_env(self):
        load_dotenv()
        appkey = os.getenv("APPKEY", "")
        secret = os.getenv("APPSECRET", "")
        if appkey and secret:
            self.key_input.setText(appkey)
            self.secret_input.setText(secret)
            self.remember_cb.setChecked(True)

    def attempt_login(self):
        appkey = self.key_input.text().strip()
        secret = self.secret_input.text().strip()
        
        if not appkey or not secret:
            QMessageBox.warning(self, "입력 오류", "APP KEY와 SECRET KEY를 모두 입력해주세요.")
            return
            
        # 체크박스 선택 시 .env 파일 생성 및 저장
        if self.remember_cb.isChecked():
            env_file = ".env"
            if not os.path.exists(env_file):
                open(env_file, 'w').close()
            set_key(env_file, "APPKEY", appkey)
            set_key(env_file, "APPSECRET", secret)
        
        # API 핸들러에 입력받은 키 값 갱신
        self.api.app_key = appkey
        self.api.app_secret = secret
        
        self.login_btn.setText("토큰 발급 요청 중...")
        self.login_btn.setEnabled(False)
        
        # 토큰 발급 시도
        success, msg = self.api.issue_token()
        print(f"토큰 발급 결과: {success}")
        if success:
            self.accept()  # QDialog 종료 신호 (성공)
            print("accept 호출")
        else:
            QMessageBox.critical(self, "인증 실패", f"토큰 발급에 실패했습니다.\n{msg}")
            self.login_btn.setText("로그인 (토큰 발급)")
            self.login_btn.setEnabled(True)

class AlgoSettingsDialog(QDialog):
    """
    매매 알고리즘 및 서버 설정 팝업창
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("알고리즘 및 서버 설정")
        self.resize(450, 200)
        layout = QVBoxLayout(self)

        # 서버 환경 설정 그룹 (수정 불가 콤보박스 + 스핀박스 유지)
        server_group = QGroupBox("매매 서버 접속 설정")
        server_layout = QHBoxLayout()
        
        server_layout.addWidget(QLabel("서버 위치:"))
        self.server_combo = QComboBox()
        self.server_combo.addItems(["메인 서버", "서브 서버 A", "서브 서버 B"])
        self.server_combo.setEditable(False) # 타이핑 비활성화
        server_layout.addWidget(self.server_combo)

        server_layout.addWidget(QLabel("서버 번호:"))
        self.server_spinbox = QSpinBox()
        self.server_spinbox.setRange(1, 99)
        server_layout.addWidget(self.server_spinbox)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)

        # 알고리즘 선택 및 시작 그룹
        algo_group = QGroupBox("매매 로직")
        algo_layout = QHBoxLayout()
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["볼린저밴드 돌파", "이동평균 크로스오버", "VWAP 스캘핑"])
        self.algo_combo.setEditable(False)
        algo_layout.addWidget(self.algo_combo)
        
        # 추후 상세 설정을 위한 버튼 추가
        edit_logic_btn = QPushButton("⚙️ 로직 상세 설정")
        algo_layout.addWidget(edit_logic_btn)
        
        start_btn = QPushButton("자동매매 시작")
        start_btn.setStyleSheet("background-color: #2b5797; color: white; font-weight: bold;")
        algo_layout.addWidget(start_btn)
        
        algo_group.setLayout(algo_layout)
        layout.addWidget(algo_group)


class HTSMainWindow(QMainWindow):
    def __init__(self, api_handler):
        super().__init__()
        self.api = api_handler
        self.setWindowTitle("개인용 HTS 프로토타입 v2")
        self.resize(1300, 850)

        # 패널 변수 초기화
        self.left_dock = None
        self.right_dock = None

        self.setup_menus()
        self.setup_left_panel()
        self.setup_right_panel()
        self.setup_central_chart()
        self.setup_bottom_ticker()

    def setup_menus(self):
        """
        상단 메뉴바 구성 (패널 복구 및 시스템 관리) 
        """
        menubar = self.menuBar()
        
        # 보기 메뉴 (창 복구용)
        view_menu = menubar.addMenu("보기(V)")
        
        show_left_action = QAction("종목 검색 및 관심종목 패널 열기", self)
        show_left_action.triggered.connect(lambda: self.left_dock.show() if self.left_dock else None)
        view_menu.addAction(show_left_action)
        
        show_right_action = QAction("주문 및 잔고 패널 열기", self)
        show_right_action.triggered.connect(lambda: self.right_dock.show() if self.right_dock else None)
        view_menu.addAction(show_right_action)

        # 시스템 관리 메뉴 (버전 관리 분리)
        sys_menu = menubar.addMenu("시스템(S)")
        
        update_action = QAction("수동 버전 확인 및 업데이트", self)
        # update_action.triggered.connect(self.check_update) # 실제 구현시 연결
        sys_menu.addAction(update_action)
        
        algo_action = QAction("알고리즘 및 서버 설정", self)
        algo_action.triggered.connect(self.open_algo_settings)
        sys_menu.addAction(algo_action)

    def setup_central_chart(self):
        # \"\"\"중앙 차트 영역 (차트 툴바 + 탭 구조)\"\"\"
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. 차트 툴바 (항상 표시됨)
        chart_toolbar = QToolBar("차트 도구")
        chart_toolbar.setMovable(False)
        
        # 봉 선택
        timeframe_combo = QComboBox()
        timeframe_combo.addItems(["일봉", "주봉", "월봉", "분봉(1분)", "분봉(3분)", "틱(10틱)"])
        chart_toolbar.addWidget(timeframe_combo)
        chart_toolbar.addSeparator()
        
        # 그리기 도구
        draw_line_action = QAction("✏️ 추세선 긋기", self)
        chart_toolbar.addAction(draw_line_action)
        
        color_btn = QPushButton("선 색상")
        color_btn.clicked.connect(self.select_color)
        chart_toolbar.addWidget(color_btn)
        chart_toolbar.addSeparator()
        
        # 보조지표
        indicator_combo = QComboBox()
        indicator_combo.addItems(["지표 추가 ▼", "이동평균선", "볼린저밴드", "MACD", "RSI"])
        chart_toolbar.addWidget(indicator_combo)
        
        # 분할 화면 버튼 (추후 구현 예정)
        chart_toolbar.addSeparator()
        split_btn = QPushButton("🪟 화면 분할(예정)")
        split_btn.setEnabled(False)
        chart_toolbar.addWidget(split_btn)

        central_layout.addWidget(chart_toolbar)

        # 2. 차트 탭 (종목별 유지)
        self.chart_tabs = QTabWidget()
        self.chart_tabs.setTabsClosable(True) # 탭 닫기 버튼 활성화
        self.chart_tabs.tabCloseRequested.connect(self.close_chart_tab)
        
        # 기본 안내 화면 (선택된 종목이 없을 때)
        default_chart = QLabel("종목을 선택하거나 검색하여 차트를 엽니다.\\n(상단 툴바를 이용해 지표 및 선 긋기 가능)")
        default_chart.setAlignment(Qt.AlignCenter)
        default_chart.setStyleSheet("background-color: #1e1e1e; color: #888888; font-size: 16px;")
        self.chart_tabs.addTab(default_chart, "기본 차트")
        
        # 삼성전자 탭 예시 (유지됨)
        samsung_chart = QLabel("📈 삼성전자 차트 영역\\n(PyQtGraph 캔들스틱 연동 예정)")
        samsung_chart.setAlignment(Qt.AlignCenter)
        samsung_chart.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-size: 20px;")
        self.chart_tabs.addTab(samsung_chart, "삼성전자")
        
        central_layout.addWidget(self.chart_tabs)
        self.setCentralWidget(central_widget)

    def close_chart_tab(self, index):
        """
        탭 닫기 기능
        """
        if self.chart_tabs.count() > 1: # 마지막 탭은 남겨둠
            self.chart_tabs.removeTab(index)

    def select_color(self):
        """
        선 색상 선택 다이얼로그
        """
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"선택된 색상: {color.name()}")
            # 실제 선 그리기 로직에 색상 반영 예정

    def setup_left_panel(self):
        self.left_dock = QDockWidget("잔고/평가 및 종목 검색", self)
        self.left_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        splitter = QSplitter(Qt.Vertical)
        
        # --- 1. 상단: 잔고/평가 영역 ---
        balance_frame = QFrame()
        balance_frame.setFrameShape(QFrame.StyledPanel)
        balance_frame.setStyleSheet("QFrame { border: 1px solid #555555; border-radius: 4px; background-color: #1e1e1e; }")
        balance_layout = QVBoxLayout(balance_frame)
        balance_layout.setSpacing(10)
        
        # [수정] Grid 효과를 위한 요약 정보 컨테이너
        summary_widget = QWidget()
        # 전체 배경을 선 색상(#555555)으로 지정하고 내부 라벨들의 배경을 따로 지정하여 테두리 구현
        summary_widget.setStyleSheet("background-color: #555555; border: none;") 
        
        summary_grid = QGridLayout(summary_widget)
        summary_grid.setSpacing(1) # 이 간격(1px)이 그리드 선 두께가 됨
        summary_grid.setContentsMargins(1, 1, 1, 1) # 바깥쪽 테두리
        
        # 공통 라벨 생성 헬퍼 함수 (반복 작업 최소화)
        def create_grid_label(text, is_title=False):
            lbl = QLabel(text)
            if is_title:
                lbl.setStyleSheet("background-color: #2d2d30; color: #d4d4d4; padding: 5px; font-weight: bold;")
                lbl.setAlignment(Qt.AlignCenter)
            else:
                lbl.setStyleSheet("background-color: #1e1e1e; color: #ffffff; padding: 5px;")
                lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return lbl

        # 1행
        summary_grid.addWidget(create_grid_label("총 손익", True), 0, 0)
        self.lbl_total_pl = create_grid_label("100000000원 (00.00%)")
        summary_grid.addWidget(self.lbl_total_pl, 0, 1)
        
        summary_grid.addWidget(create_grid_label("예수금", True), 0, 2)
        self.lbl_deposit = create_grid_label("10000000000원")
        summary_grid.addWidget(self.lbl_deposit, 0, 3)

        # 2행
        summary_grid.addWidget(create_grid_label("총 매입", True), 1, 0)
        self.lbl_total_buy = create_grid_label("10000000원")
        summary_grid.addWidget(self.lbl_total_buy, 1, 1)
        
        summary_grid.addWidget(create_grid_label("총 평가", True), 1, 2)
        self.lbl_total_eval = create_grid_label("10000000원")
        summary_grid.addWidget(self.lbl_total_eval, 1, 3)

        # 3행
        summary_grid.addWidget(create_grid_label("실현손익", True), 2, 0)
        self.lbl_realized_pl = create_grid_label("110000000000원")
        summary_grid.addWidget(self.lbl_realized_pl, 2, 1)

        # 빈칸 채우기용 (그리드 모양 유지를 위함)
        summary_grid.addWidget(create_grid_label("D+2 추정금", True), 2, 2)
        self.lbl_d2_deposit = create_grid_label("10000000000원")
        summary_grid.addWidget(self.lbl_d2_deposit, 2, 3)

        balance_layout.addWidget(summary_widget)
        
        # 구분선 및 종목 현황 타이틀
        balance_layout.addWidget(QLabel("<b>종목 현황</b>"))
        
        # 종목 현황 테이블 세팅 (이전과 동일)
        self.balance_table = QTableWidget(1, 6) 
        self.balance_table.setHorizontalHeaderLabels([
            "종목명", "매입가/현재가", "보유수량", "평가손익(수익률)", "매입/평가금액", "수수료/세금"
        ])
        self.balance_table.setShowGrid(True)
        self.balance_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #555555;
                border: 1px solid #444444;
                background-color: #1e1e1e;
            }
            QHeaderView::section {
                background-color: #2d2d30;
                border: 1px solid #555555;
                padding: 4px;
                font-weight: bold;
            }
            QTableWidget::item {
                border-right: 1px solid #333333;
                border-bottom: 1px solid #333333;
                padding: 4px;
            }
        """)
        self.balance_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.balance_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        balance_layout.addWidget(self.balance_table)
        splitter.addWidget(balance_frame)

        # --- 2. 하단: 종목 검색 및 관심종목 영역 ---
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("종목명 또는 코드 검색 (예: 삼성전자)")
        search_layout.addWidget(self.search_box)
        self.fav_tree = QTreeWidget()
        self.fav_tree.setHeaderLabel("관심종목 그룹")
        search_layout.addWidget(self.fav_tree)
        splitter.addWidget(search_widget)
        
        splitter.setSizes([600, 400])
        self.left_dock.setWidget(splitter)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)
    def setup_right_panel(self):
        self.right_dock = QDockWidget("주문 및 미체결", self)
        self.right_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        
        layout.addWidget(QLabel("◆ 호가창"))
        self.hoga_table = QTableWidget(10, 3)
        self.hoga_table.setHorizontalHeaderLabels(["매도잔량", "호가", "매수잔량"])
        self.hoga_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hoga_table.verticalHeader().setVisible(False)
        layout.addWidget(self.hoga_table)
        
        order_group = QGroupBox("◆ 매수/매도 주문")
        order_layout = QVBoxLayout()
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("주문구분:"))
        self.order_type = QComboBox()
        self.order_type.addItems(["지정가", "시장가", "조건부지정가"])
        self.order_type.setEditable(False)
        type_layout.addWidget(self.order_type)
        order_layout.addLayout(type_layout)
        
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("주문단가:"))
        self.price_spin = QSpinBox()
        self.price_spin.setRange(0, 10000000)
        self.price_spin.setSingleStep(100)
        price_layout.addWidget(self.price_spin)
        order_layout.addLayout(price_layout)
        
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("주문수량:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, 100000)
        qty_layout.addWidget(self.qty_spin)
        order_layout.addLayout(qty_layout)
        
        btn_layout = QHBoxLayout()
        buy_btn = QPushButton("매 수")
        buy_btn.setStyleSheet("color: red; font-weight: bold;")
        sell_btn = QPushButton("매 도")
        sell_btn.setStyleSheet("color: blue; font-weight: bold;")
        btn_layout.addWidget(buy_btn)
        btn_layout.addWidget(sell_btn)
        order_layout.addLayout(btn_layout)
        
        order_group.setLayout(order_layout)
        layout.addWidget(order_group)
        
        self.balance_tabs = QTabWidget()
        self.balance_tabs.addTab(QLabel("미체결 내역 리스트"), "미체결")
        layout.addWidget(self.balance_tabs)
        
        self.right_dock.setWidget(container)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

    def setup_bottom_ticker(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        self.ticker_label = QLabel()
        self.ticker_label.setStyleSheet("color: #ff9900; font-weight: bold; font-size: 13px;")
        self.statusbar.addWidget(self.ticker_label)
        
        self.ticker_messages = [
            "[시스템] 키움 API 모의투자 서버 연결 완료",
            "[체결알림] 삼성전자 50주 @ 75,000원 매수 체결 완료",
            "[내 수익률] 총 평가손익: +125,000원 (+1.25%)"
        ]
        self.current_ticker_idx = 0
        self.update_ticker()
        
        self.ticker_timer = QTimer(self)
        self.ticker_timer.timeout.connect(self.update_ticker)
        self.ticker_timer.start(3000)

    def update_ticker(self):
        self.ticker_label.setText("  ▶  " + self.ticker_messages[self.current_ticker_idx])
        self.current_ticker_idx = (self.current_ticker_idx + 1) % len(self.ticker_messages)

    def open_algo_settings(self):
        dialog = AlgoSettingsDialog(self)
        dialog.exec()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 1. API 핸들러 인스턴스를 빈 키로 먼저 생성합니다.
    kiwoom_api = KiwoomRestAPI(app_key="", app_secret="", is_mock=True)
    
    # 2. 로그인 창을 띄우고 API 핸들러를 넘겨줍니다.
    login_dialog = LoginDialog(kiwoom_api)

    # 3. exec()는 창이 닫힐 때까지 코드를 멈추고 대기합니다.
    # 로그인이 성공하여 self.accept()가 호출되면 QDialog.Accepted가 반환됩니다.
    if login_dialog.exec() == QDialog.Accepted:
        
        # 4. 토큰 발급이 정상적으로 완료되었으므로 메인 UI를 실행합니다.
        # 기존 HTSMainWindow의 __init__에 api_handler를 받을 수 있도록 수정해야 합니다.
        window = HTSMainWindow(api_handler=kiwoom_api) 
        window.show()
        sys.exit(app.exec())
    else:
        # 로그인 창을 그냥 'X' 버튼으로 끄거나 취소하면 프로그램이 완전히 종료됩니다.
        sys.exit()