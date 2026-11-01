import sys, os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QDockWidget, QLabel, QLineEdit,
                               QTreeWidget, QTreeWidgetItem, QTableWidget, 
                               QTabWidget, QComboBox, QSpinBox, QPushButton, 
                               QStatusBar, QDialog, QGroupBox, QHeaderView, 
                               QToolBar, QMenuBar, QColorDialog, QCheckBox, QMessageBox,
                               QSplitter, QFrame, QGridLayout, QTableWidgetItem, QCompleter, QAbstractItemView,QMenu)
from PySide6.QtCore import Qt, QTimer, QStringListModel, QRectF
from PySide6.QtGui import QAction, QColor, QPainter, QPicture, QCursor
import pyqtgraph as pg

from dotenv import load_dotenv, set_key

# --- 분리된 모듈 임포트 ---
from kiwoom_api import KiwoomRestAPI
from Workers import SystemInitWorker, ChartDataWorker, KiwoomWebSocketWorker, HogaDataWorker, BalanceDataWorker

            
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

class BalanceDialog(QDialog):
    def __init__(self, parent, api_handler):
        super().__init__(parent)
        self.api = api_handler
        self.setWindowTitle("내 잔고 및 평가 현황")
        self.resize(800, 400)
        
        # 전체 레이아웃
        self.layout = QVBoxLayout(self)
        
        # 안내 메시지 바
        self.status_label = QLabel("데이터를 불러오는 중입니다...")
        self.status_label.setStyleSheet("color: #ff9900; font-weight: bold;")
        self.layout.addWidget(self.status_label)
        
        # --- 상단: 요약 그리드 ---
        summary_widget = QWidget()
        summary_widget.setStyleSheet("background-color: #555555; border: none;") 
        summary_grid = QGridLayout(summary_widget)
        summary_grid.setSpacing(1)
        summary_grid.setContentsMargins(1, 1, 1, 1)
        
        def create_grid_label(text, is_title=False):
            lbl = QLabel(text)
            if is_title:
                lbl.setStyleSheet("background-color: #2d2d30; color: #d4d4d4; padding: 5px; font-weight: bold;")
                lbl.setAlignment(Qt.AlignCenter)
            else:
                lbl.setStyleSheet("background-color: #1e1e1e; color: #ffffff; padding: 5px;")
                lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            return lbl

        summary_grid.addWidget(create_grid_label("총 손익", True), 0, 0)
        self.lbl_total_pl = create_grid_label("0원 (0.00%)")
        summary_grid.addWidget(self.lbl_total_pl, 0, 1)
        
        summary_grid.addWidget(create_grid_label("예수금", True), 0, 2)
        self.lbl_deposit = create_grid_label("0원")
        summary_grid.addWidget(self.lbl_deposit, 0, 3)

        summary_grid.addWidget(create_grid_label("총 매입", True), 1, 0)
        self.lbl_total_buy = create_grid_label("0원")
        summary_grid.addWidget(self.lbl_total_buy, 1, 1)
        
        summary_grid.addWidget(create_grid_label("총 평가", True), 1, 2)
        self.lbl_total_eval = create_grid_label("0원")
        summary_grid.addWidget(self.lbl_total_eval, 1, 3)

        summary_grid.addWidget(create_grid_label("실현손익", True), 2, 0)
        self.lbl_realized_pl = create_grid_label("0원")
        summary_grid.addWidget(self.lbl_realized_pl, 2, 1)

        summary_grid.addWidget(create_grid_label("D+2 추정금", True), 2, 2)
        self.lbl_d2_deposit = create_grid_label("0원")
        summary_grid.addWidget(self.lbl_d2_deposit, 2, 3)

        self.layout.addWidget(summary_widget)
        
        # --- 하단: 종목 현황 테이블 ---
        self.balance_table = QTableWidget(0, 6) 
        self.balance_table.setHorizontalHeaderLabels([
            "종목명", "매입가/현재가", "보유수량", "평가손익(수익률)", "매입/평가금액", "수수료/세금"
        ])
        self.balance_table.setShowGrid(True)
        self.balance_table.setStyleSheet("""
            QTableWidget { gridline-color: #555555; border: 1px solid #555555; background-color: #1e1e1e; color: #ffffff; }
            QHeaderView::section { background-color: #2d2d30; color: #d4d4d4; border: 1px solid #555555; padding: 4px; font-weight: bold; }
            QTableWidget::item { border-right: 1px solid #333333; border-bottom: 1px solid #333333; padding: 4px; }
        """)
        self.balance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.balance_table)
        
        # 다이얼로그 렌더링 시 최신 데이터 호출
        self.fetch_balance_data()

    def fetch_balance_data(self):
        """가벼운 잔고 전용 워커를 실행합니다."""
        self.worker = BalanceDataWorker(self.api)
        self.worker.finished.connect(self.update_ui)
        self.worker.start()

    def get_color_by_value(self, value):
        try:
            val = float(value)
            if val > 0: return QColor("#ff4c4c")
            elif val < 0: return QColor("#4c8cff")
            else: return QColor("#ffffff")
        except ValueError: return QColor("#ffffff")

    def update_ui(self, success, data):
        if not success:
            self.status_label.setText(f"데이터 조회 실패: {data.get('return_msg', '알 수 없는 오류')}")
            return
            
        self.status_label.setText("잔고 및 평가 현황 갱신 완료")
        
        # --- 1. 상단 요약 그리드 파싱 및 업데이트 ---
        tot_pl = int(data.get("tot_evlt_pl", 0))      
        tot_rt = float(data.get("tot_prft_rt", 0.0))  
        tot_buy = int(data.get("tot_pur_amt", 0))     
        tot_eval = int(data.get("tot_evlt_amt", 0))   
        deposit = int(data.get("prsm_dpst_aset_amt", 0)) 
        
        realized_pl = int(data.get("rlzt_pl", 0))
        
        # 라벨 텍스트 적용
        self.lbl_total_buy.setText(f"{tot_buy:,}원")
        self.lbl_total_eval.setText(f"{tot_eval:,}원")
        self.lbl_deposit.setText(f"{deposit:,}원")
        self.lbl_d2_deposit.setText(f"{deposit:,}원")
        
        # 색상 적용 (총 평가손익 및 실현손익)
        self.lbl_total_pl.setText(f"{tot_pl:,}원 ({tot_rt}%)")
        self.lbl_total_pl.setStyleSheet(f"background-color: #1e1e1e; color: {self.get_color_by_value(tot_pl).name()}; padding: 5px;")
        
        self.lbl_realized_pl.setText(f"{realized_pl:,}원")
        self.lbl_realized_pl.setStyleSheet(f"background-color: #1e1e1e; color: {self.get_color_by_value(realized_pl).name()}; padding: 5px;")

        # --- 2. 하단 종목 현황 테이블 파싱 및 업데이트 ---
        stock_list = data.get("acnt_evlt_remn_indv_tot", [])
        self.balance_table.setRowCount(len(stock_list))
        
        for row, stock in enumerate(stock_list):
            stk_nm = stock.get("stk_nm", "")
            
            pur_pric = int(stock.get("pur_pric", 0))
            cur_prc = int(stock.get("cur_prc", 0))
            price_txt = f"{pur_pric:,} / {cur_prc:,}"
            
            qty = int(stock.get("rmnd_qty", 0))
            
            evltv_prft = int(stock.get("evltv_prft", 0))
            prft_rt = float(stock.get("prft_rt", 0.0))
            pl_txt = f"{evltv_prft:,} ({prft_rt}%)"
            
            pur_amt = int(stock.get("pur_amt", 0))
            evlt_amt = int(stock.get("evlt_amt", 0))
            amt_txt = f"{pur_amt:,} / {evlt_amt:,}"
            
            sum_cmsn = int(stock.get("sum_cmsn", 0))
            tax = int(stock.get("tax", 0))
            fee_txt = f"{sum_cmsn:,} / {tax:,}"

            # 테이블 아이템 생성
            items = [
                QTableWidgetItem(stk_nm),
                QTableWidgetItem(price_txt),
                QTableWidgetItem(f"{qty:,}"),
                QTableWidgetItem(pl_txt),
                QTableWidgetItem(amt_txt),
                QTableWidgetItem(fee_txt)
            ]

            # 4번째 열(인덱스 3): 평가손익(수익률) 빨강/파랑 색상 적용
            items[3].setForeground(self.get_color_by_value(evltv_prft))

            # 정렬 후 셀에 추가
            for col, item in enumerate(items):
                if col == 0:
                    item.setTextAlignment(Qt.AlignCenter) # 종목명은 중앙 정렬
                else:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter) # 숫자는 우측 정렬
                self.balance_table.setItem(row, col, item)

pg.setConfigOption('background', '#1e1e1e')
pg.setConfigOption('foreground', '#d4d4d4')

class CandlestickItem(pg.GraphicsObject):
    """PyQtGraph를 이용한 캔들스틱 렌더링 커스텀 아이템"""
    def __init__(self, data):
        super().__init__()
        self.data = data  # data = [(t, open, high, low, close, volume), ...]
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = 0.3 # 캔들 몸통 두께
        
        for (t, open, high, low, close, volume) in self.data:
            # 양봉(빨강), 음봉(파랑), 보합(흰색)
            if close > open:
                p.setPen(pg.mkPen('#ff4c4c'))
                p.setBrush(pg.mkBrush('#ff4c4c'))
            elif close < open:
                p.setPen(pg.mkPen('#4c8cff'))
                p.setBrush(pg.mkBrush('#4c8cff'))
            else:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
                
            # 꼬리 그리기 (High-Low)
            p.drawLine(pg.Point(t, low), pg.Point(t, high))
            # 몸통 그리기 (Open-Close)
            p.drawRect(QRectF(t - w, open, w * 2, close - open))
            
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())  
# ---  X축 시간 표시 커스텀 축 ---
class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_labels = {} # {index: "시간포맷"}

    def update_labels(self, labels_dict):
        self.x_labels = labels_dict

    def tickStrings(self, values, scale, spacing):
        # 500, 501 같은 숫자를 "10:30" 같은 시간 문자열로 변환
        return [self.x_labels.get(int(value), "") for value in values]

# ---  Y축 가격 콤마 표시 커스텀 축 ---
class PriceAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [f"{int(value):,}" for value in values]



# --- 독립된 1개의 차트 탭 위젯 (툴바 + 십자선 + 정보표시 통합) ---
class SingleChartTab(QWidget):
    def __init__(self, parent_main, stock_code, initial_tf="분봉(5분)"):
        super().__init__()
        self.main_ui = parent_main
        self.stock_code = stock_code
        self.chart_data = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 1) 개별 탭 툴바
        self.toolbar = QToolBar()
        self.tf_combo = QComboBox()
        self.tf_combo.addItems(["일봉", "주봉", "월봉", "분봉(1분)", "분봉(3분)", "분봉(5분)", "틱(10틱)"])
        self.tf_combo.setCurrentText(initial_tf)
        self.tf_combo.setMinimumWidth(100) # [수정] 글자가 잘리지 않도록 최소 너비 확장
        self.tf_combo.currentTextChanged.connect(self.request_new_data)
        self.toolbar.addWidget(self.tf_combo)
        
        self.toolbar.addSeparator()
        self.toolbar.addAction("✏️ 추세선")
        self.toolbar.addWidget(QPushButton("선 색상"))
        self.toolbar.addSeparator()
        
        # [수정] 지표 추가 콤보박스 부활
        self.indicator_combo = QComboBox()
        self.indicator_combo.addItems(["지표 추가 ▼", "이동평균선", "볼린저밴드", "MACD", "RSI"])
        self.indicator_combo.setMinimumWidth(110)
        self.toolbar.addWidget(self.indicator_combo)
        
        self.info_label = QLabel(" 차트에 마우스를 올리면 정보가 표시됩니다.")
        self.info_label.setStyleSheet("color: #ffcc00; font-weight: bold; padding: 2px;")
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.info_label)

        # 2) 차트 뷰 생성
        self.x_axis = TimeAxisItem(orientation='bottom')
        self.y_axis = PriceAxisItem(orientation='left')
        self.chart_view = pg.PlotWidget(axisItems={'bottom': self.x_axis, 'left': self.y_axis})
        self.chart_view.showGrid(x=True, y=True, alpha=0.3)
        
        # [수정] pyqtgraph 기본 우클릭 메뉴 비활성화 및 커스텀 메뉴 연결
        self.chart_view.setMenuEnabled(False) 
        self.chart_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chart_view.customContextMenuRequested.connect(self.show_custom_context_menu)
        
        # [수정] 마우스 조작: 세로 이동/확대 금지 (가로로만 이동/확대 가능)
        self.chart_view.getViewBox().setMouseEnabled(x=True, y=False)
        # 가로 범위(X축)가 바뀔 때마다 Y축(가격) 범위를 자동으로 맞추는 시그널 연결
        self.chart_view.getViewBox().sigXRangeChanged.connect(self.update_y_auto_scale)

        layout.addWidget(self.chart_view)

        # 3) 십자선 세팅
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen(color='gray', style=Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen(color='gray', style=Qt.DashLine))
        self.chart_view.addItem(self.vLine, ignoreBounds=True)
        self.chart_view.addItem(self.hLine, ignoreBounds=True)
        
        self.proxy = pg.SignalProxy(self.chart_view.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.request_new_data()

    def show_custom_context_menu(self, pos):
        """우클릭 시 호출되는 우리가 만든 커스텀 메뉴"""
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #2d2d30; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #3e3e42; }")
        
        fav_action = QAction(f"⭐ '{self.stock_code}' 즐겨찾기 추가", self)
        # fav_action.triggered.connect(...) # 나중에 즐겨찾기 트리와 연결
        menu.addAction(fav_action)
        
        menu.addSeparator()
        
        buy_action = QAction(f"🔴 '{self.stock_code}' 매수 주문", self)
        sell_action = QAction(f"🔵 '{self.stock_code}' 매도 주문", self)
        menu.addAction(buy_action)
        menu.addAction(sell_action)
        
        menu.exec_(QCursor.pos())

    def update_y_auto_scale(self):
        """현재 화면에 보이는 X축 범위 내의 봉들만 계산해서 Y축(가격) 높낮이를 자동 조절합니다."""
        if not self.chart_data: return
        
        # 현재 화면에 보이는 X축 최소/최대 인덱스
        view_range = self.chart_view.viewRange()
        x_min, x_max = int(view_range[0][0]), int(view_range[0][1])
        
        # 데이터 범위를 벗어나지 않게 보정
        x_min = max(0, x_min)
        x_max = min(len(self.chart_data) - 1, x_max)
        
        if x_min >= x_max: return
        
        # 보이는 범위 내의 고가(High)와 저가(Low) 수집
        visible_data = self.chart_data[x_min:x_max+1]
        max_price = max([row[2] for row in visible_data])
        min_price = min([row[3] for row in visible_data])
        
        # 위아래 5% 여백을 두고 Y축 강제 고정
        margin = (max_price - min_price) * 0.05
        if margin == 0: margin = max_price * 0.01
        self.chart_view.getViewBox().setYRange(min_price - margin, max_price + margin, padding=0)

    def request_new_data(self):
        """콤보박스 변경 시 자신의 탭 데이터만 다시 불러옴"""
        selected_tf = self.tf_combo.currentText()
        # 주의: 메인 창의 api 객체를 참조함
        self.worker = ChartDataWorker(self.main_ui.api, self.stock_code, selected_tf)
        self.worker.finished.connect(self.draw_chart)
        self.worker.start()

    def draw_chart(self, success, stock_code, chart_data):
        if not success or not chart_data: return
        self.chart_data = chart_data
        self.chart_view.clear() # 기존 캔들 삭제
        self.chart_view.addItem(self.vLine, ignoreBounds=True)
        self.chart_view.addItem(self.hLine, ignoreBounds=True)
        
        # X축 시간 매핑 데이터 생성 (포맷팅)
        x_dict = {}
        for (i, o, h, l, c, v, dt_str) in chart_data:
            # 예: "20261101153000" -> "11/01 15:30", "20261101" -> "11/01"
            if len(dt_str) >= 12: 
                fmt_str = f"{dt_str[4:6]}/{dt_str[6:8]} {dt_str[8:10]}:{dt_str[10:12]}"
            else:
                fmt_str = f"{dt_str[0:4]}/{dt_str[4:6]}/{dt_str[6:8]}"
            x_dict[i] = fmt_str
            
        self.x_axis.update_labels(x_dict)
        
        # 캔들스틱 그리기 (시간 튜플에서 time_str을 제외하고 넘김)
        pure_ohlc = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in chart_data]
        candlestick = CandlestickItem(pure_ohlc)
        self.chart_view.addItem(candlestick)
        
        # 확대/축소 제한 (Limits) 설정
        # y축 최소/최고가 찾기
        min_y = min([row[3] for row in chart_data])
        max_y = max([row[2] for row in chart_data])
        margin = (max_y - min_y) * 0.1
        
        # # x축은 -5 ~ 데이터길이+5 까지만 이동 가능하게 제한
        # self.chart_view.setLimits(xMin=-5, xMax=len(chart_data)+5, 
        #                           yMin=min_y - margin, yMax=max_y + margin)
        self.chart_view.autoRange()

    def mouseMoved(self, evt):
        pos = evt[0]
        if self.chart_view.sceneBoundingRect().contains(pos):
            mousePoint = self.chart_view.plotItem.vb.mapSceneToView(pos)
            index = int(round(mousePoint.x()))
            
            # 십자선 이동
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
            
            # 인덱스가 데이터 범위 안일 때 상단 라벨에 OHLC 업데이트
            if 0 <= index < len(self.chart_data):
                row = self.chart_data[index]
                time_val = self.x_axis.x_labels.get(index, "")
                o, h, l, c, v = row[1], row[2], row[3], row[4], row[5]
                # 등락률 계산 (전 캔들 대비가 아닌 단순히 시가 대비로 임시 표시, API에서 전일대비 받아와서 적용가능)
                self.info_label.setText(
                    f"[{time_val}]  시가: {o:,}  고가: {h:,}  저가: {l:,}  종가: {c:,}  거래량: {v:,}"
                )


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
        self.setup_right_panel()
        self.setup_central_chart()
        self.setup_bottom_ticker()

    def setup_menus(self):
        """상단 메뉴바 구성"""
        menubar = self.menuBar()
        
        # 보기 메뉴 (우측 주문 패널 복구용만 남김)
        view_menu = menubar.addMenu("보기(V)")
        show_right_action = QAction("종목 검색 및 주문 패널 열기", self)
        show_right_action.triggered.connect(lambda: self.right_dock.show() if self.right_dock else None)
        view_menu.addAction(show_right_action)

        # 시스템 관리 메뉴
        sys_menu = menubar.addMenu("시스템(S)")
        update_action = QAction("수동 버전 확인 및 업데이트", self)
        sys_menu.addAction(update_action)
        
        algo_action = QAction("알고리즘 및 서버 설정", self)
        algo_action.triggered.connect(self.open_algo_settings)
        sys_menu.addAction(algo_action)

    def setup_central_chart(self):
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        
        # [수정] 메인 툴바를 다시 살려서 프로그램 전역 기능(잔고조회 등) 배치
        main_toolbar = QToolBar("메인 도구")
        main_toolbar.setMovable(False)
        main_toolbar.setStyleSheet("background-color: #252526; border-bottom: 1px solid #333;")
        
        balance_btn = QPushButton("💰 내 잔고 현황 (새창)")
        balance_btn.setStyleSheet("background-color: #2b5797; color: white; font-weight: bold; padding: 6px 12px; margin: 2px;")
        balance_btn.clicked.connect(self.open_balance_dialog)
        main_toolbar.addWidget(balance_btn)
        
        central_layout.addWidget(main_toolbar)

        self.chart_tabs = QTabWidget()
        self.chart_tabs.setTabsClosable(True)
        self.chart_tabs.tabCloseRequested.connect(self.close_chart_tab)
        
        default_chart = QLabel("종목을 검색하면 독립된 차트 탭이 생성됩니다.")
        default_chart.setAlignment(Qt.AlignCenter)
        default_chart.setStyleSheet("background-color: #1e1e1e; color: #888888; font-size: 16px;")
        self.chart_tabs.addTab(default_chart, "기본 차트")
        
        central_layout.addWidget(self.chart_tabs)
        self.setCentralWidget(central_widget)

        
    def open_balance_dialog(self):
            dialog = BalanceDialog(self, self.api)
            dialog.exec()

    def close_chart_tab(self, index):
        if self.chart_tabs.count() > 1:
            self.chart_tabs.removeTab(index)


    def select_color(self):
        """
        선 색상 선택 다이얼로그
        """
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"선택된 색상: {color.name()}")
            # 실제 선 그리기 로직에 색상 반영 예정

    

    def setup_right_panel(self):
        self.right_dock = QDockWidget("종목 검색 및 주문", self)
        self.right_dock.setAllowedAreas(Qt.RightDockWidgetArea)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        
        # --- 1. 상단: 종목 검색 및 관심종목 ---
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("종목검색:"))
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("종목명 또는 코드 검색 후 Enter")
        search_layout.addWidget(self.search_box)
        layout.addLayout(search_layout)
        
        self.fav_tree = QTreeWidget()
        self.fav_tree.setHeaderLabel("관심종목 그룹")
        self.fav_tree.setMaximumHeight(120) # 공간 확보를 위해 높이 제한
        layout.addWidget(self.fav_tree)
        
        # --- 2. 중단: 호가창과 주문창 병렬 배치 (QHBoxLayout) ---
        hoga_order_layout = QHBoxLayout()
        
        # 호가창 설정 (기존과 동일하되 가로 공간 공유)
        self.hoga_table = QTableWidget(10, 3)
        self.hoga_table.setHorizontalHeaderLabels(["매도잔량", "호가", "매수잔량"])
        self.hoga_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hoga_table.verticalHeader().setVisible(False)
        self.hoga_table.setShowGrid(True)
        # (테이블 스타일시트는 기존 table_css 적용)
        hoga_order_layout.addWidget(self.hoga_table, stretch=1) 
        
        # 매수/매도 주문 패널
        order_group = QGroupBox("주문")
        order_layout = QVBoxLayout(order_group)
        
        self.order_type = QComboBox()
        self.order_type.addItems(["지정가", "시장가", "조건부지정가"])
        order_layout.addWidget(self.order_type)
        
        self.price_spin = QSpinBox()
        self.price_spin.setPrefix("단가: ")
        self.price_spin.setRange(0, 10000000)
        self.price_spin.setSingleStep(100)
        order_layout.addWidget(self.price_spin)
        
        self.qty_spin = QSpinBox()
        self.qty_spin.setPrefix("수량: ")
        self.qty_spin.setRange(1, 100000)
        order_layout.addWidget(self.qty_spin)
        
        buy_btn = QPushButton("매 수")
        buy_btn.setStyleSheet("background-color: #3b1e1e; color: #ff4c4c; font-weight: bold; padding: 10px;")
        sell_btn = QPushButton("매 도")
        sell_btn.setStyleSheet("background-color: #1e253b; color: #4c8cff; font-weight: bold; padding: 10px;")
        order_layout.addWidget(buy_btn)
        order_layout.addWidget(sell_btn)
        
        hoga_order_layout.addWidget(order_group, stretch=1)
        layout.addLayout(hoga_order_layout)
        
        # --- 3. 하단: 미체결 내역 (취소/정정 버튼 추가) ---
        self.unfilled_tabs = QTabWidget()
        self.unfilled_table = QTableWidget(1, 7) # 열 개수 6 -> 7 증가
        self.unfilled_table.setHorizontalHeaderLabels([
            "주문번호", "종목명", "구분", "단가", "잔량", "상태", "작업"
        ])
        self.unfilled_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 작업 버튼 셀 생성 (은은한 노란색, 초록색 적용)
        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(2, 2, 2, 2)
        btn_layout.setSpacing(4)
        
        modify_btn = QPushButton("정정")
        modify_btn.setStyleSheet("background-color: #3a5c43; color: #a4d4b4; border-radius: 2px;") # 은은한 초록
        
        cancel_btn = QPushButton("취소")
        cancel_btn.setStyleSheet("background-color: #5c553a; color: #d4c8a4; border-radius: 2px;") # 은은한 노랑
        
        btn_layout.addWidget(modify_btn)
        btn_layout.addWidget(cancel_btn)
        
        self.unfilled_table.setCellWidget(0, 6, btn_widget) # 6번 인덱스(작업 열)에 위젯 삽입

        self.unfilled_tabs.addTab(self.unfilled_table, "미체결 내역")
        layout.addWidget(self.unfilled_tabs)
        
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

    def fetch_initial_data(self):
        """앱 시작 시 잔고와 종목 마스터 데이터를 긁어옵니다."""
        self.statusbar.showMessage("시스템 초기화 및 데이터 로딩 중...")
        self.init_worker = SystemInitWorker(self.api)
        # 3개의 리스트(bool, dict, list)를 반환하는 시그널 연결
        self.init_worker.finished.connect(self.update_initial_ui)
        self.init_worker.start()

    def update_initial_ui(self, success, balance_data, master_list):
        if not success:
            self.statusbar.showMessage("초기화 통신 에러 발생", 5000)
            return

        # --- [추가] 1. 데이터를 인스턴스 변수에 영구 저장 ---
        self.current_balance_data = balance_data
        
        # 검색 효율을 위해 딕셔너리로 가공 (O(1) 속도로 찾기 위함)
        # 예: self.stock_dict["삼성전자 (005930)"] = "005930"
        self.stock_dict = {}
        for stock_str in master_list:
            # "삼성전자 (005930)" 형태에서 종목명과 코드를 분리
            try:
                name, code_with_bracket = stock_str.split(" (")
                code = code_with_bracket.replace(")", "")
                
                # 3가지 방식으로 모두 검색 가능하게 저장
                self.stock_dict[stock_str] = code # 자동완성 풀 텍스트
                self.stock_dict[name] = code      # 이름만 입력했을 때
                self.stock_dict[code] = code      # 코드만 입력했을 때
            except ValueError:
                continue
        
        # 3. 검색창 자동완성 (QCompleter) 세팅
        if master_list:
            model = QStringListModel(master_list)
            completer = QCompleter()
            completer.setModel(model)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            
            self.search_box.setCompleter(completer)
            
            # --- [추가] 4. 검색창에서 엔터키를 쳤을 때 실행될 함수 연결 ---
            # 주의: 중복 연결을 막기 위해 기존 연결을 끊고 다시 연결 (초기화를 여러 번 할 경우 대비)
            try:
                self.search_box.returnPressed.disconnect()
            except RuntimeError:
                pass
            self.search_box.returnPressed.connect(self.search_stock_action)
            
            self.statusbar.showMessage(f"초기화 완료 (종목 {len(master_list)}개 로드)", 3000)

    def search_stock_action(self):
        search_text = self.search_box.text().strip()
        if not search_text: return
        
        stock_code = self.stock_dict.get(search_text)
        if stock_code:
            self.statusbar.showMessage(f"[{stock_code}] 데이터 조회 중...", 3000)
            self.search_box.clearFocus()
            
            # --- 1. 새로운 5분봉 전용 탭을 생성해서 탭에 끼워넣기 ---
            new_tab = SingleChartTab(self, stock_code, initial_tf="분봉(5분)")
            # 탭 제목에 종목명과 코드 표시 (딕셔너리 키를 활용하거나 역방향 탐색)
            stock_name = search_text.split(" (")[0] 
            tab_index = self.chart_tabs.addTab(new_tab, f"{stock_name} ({stock_code})")
            self.chart_tabs.setCurrentIndex(tab_index) # 생성한 탭으로 화면 전환
            
            # --- 2. 호가창 주기적 갱신 세팅 ---
            self.current_hoga_code = stock_code
            self.request_hoga_update()
            if not hasattr(self, 'hoga_timer'):
                self.hoga_timer = QTimer(self)
                self.hoga_timer.timeout.connect(self.request_hoga_update)
            self.hoga_timer.start(1500) 
        else:
            self.statusbar.showMessage(f"해당 종목을 찾을 수 없습니다: {search_text}", 5000)
    

    def update_chart_ui(self, success, stock_code, chart_data):
        """ChartDataWorker 완료 시 캔들스틱을 렌더링합니다."""
        if not success or not chart_data:
            self.statusbar.showMessage(f"[{stock_code}] 차트 데이터 조회 실패", 5000)
            return
            
        self.chart_view.clear()
        
        # 커스텀 캔들스틱 아이템 생성 후 뷰에 추가
        candlestick = CandlestickItem(chart_data)
        self.chart_view.addItem(candlestick)
        self.chart_view.setTitle(f"[{stock_code}] {self.timeframe_combo.currentText()}")
        
        # 차트 높낮이 자동 맞춤
        self.chart_view.autoRange()

    def request_hoga_update(self):
        """1.5초마다 호출되어 최신 호가를 요청합니다."""
        if hasattr(self, 'current_hoga_code') and self.current_hoga_code:
            
            self.hoga_worker = HogaDataWorker(self.api, self.current_hoga_code)
            self.hoga_worker.finished.connect(self.update_hoga_table_ui)
            self.hoga_worker.start()
    
    def update_hoga_table_ui(self, success, stock_code, data):
        """5호가 기준으로 총 10행만 깔끔하게 렌더링하고, 셀 재사용으로 깜빡임을 없앱니다."""
        if not success or not data: return
        
        DISPLAY_LEVELS = 5 
        TOTAL_ROWS = DISPLAY_LEVELS * 2 # 매도 5 + 매수 5 = 10행
        
        if self.hoga_table.rowCount() != TOTAL_ROWS:
            self.hoga_table.setRowCount(TOTAL_ROWS)
            self.hoga_table.clearContents()

        # 워커에서 10호가를 다 가져왔더라도 UI에는 핵심 5호가만 잘라냅니다.
        ask_prices = data.get("ask_prices", [])
        ask_vols = data.get("ask_vols", [])
        bid_prices = data.get("bid_prices", [])
        bid_vols = data.get("bid_vols", [])
        
        if len(ask_prices) < 10 or len(bid_prices) < 10:
            return

        # 매도 배열은 역순이므로 끝에서 5개(5~1호가), 매수 배열은 앞에서 5개(1~5호가) 추출
        disp_ask_prices = ask_prices[-DISPLAY_LEVELS:]
        disp_ask_vols = ask_vols[-DISPLAY_LEVELS:]
        disp_bid_prices = bid_prices[:DISPLAY_LEVELS]
        disp_bid_vols = bid_vols[:DISPLAY_LEVELS]

        # --- 셀 업데이트 헬퍼 (플리커링 방지) ---
        # 매초 clearContents()를 하면 화면이 깜빡이고 스크롤이 튀므로, 기존 셀의 글자만 바꿉니다.
        def set_cell(row, col, text, align, fg_color=None, bg_color=None):
            item = self.hoga_table.item(row, col)
            if not item:
                item = QTableWidgetItem(text)
                self.hoga_table.setItem(row, col, item)
            else:
                item.setText(text)
            
            item.setTextAlignment(align)
            if fg_color: item.setForeground(QColor(fg_color))
            if bg_color: item.setBackground(QColor(bg_color))

        # 매도 호가 그리기 (상단 5칸)
        for i in range(DISPLAY_LEVELS):
            set_cell(i, 0, f"{disp_ask_vols[i]:,}", Qt.AlignRight | Qt.AlignVCenter, fg_color="#4c8cff")
            set_cell(i, 1, f"{disp_ask_prices[i]:,}", Qt.AlignCenter, bg_color="#1a2b4c")
            set_cell(i, 2, "", Qt.AlignCenter) # 반대편 잔량 비우기

        # 매수 호가 그리기 (하단 5칸)
        for i in range(DISPLAY_LEVELS):
            row = i + DISPLAY_LEVELS
            set_cell(row, 0, "", Qt.AlignCenter) # 반대편 잔량 비우기
            set_cell(row, 1, f"{disp_bid_prices[i]:,}", Qt.AlignCenter, bg_color="#4c1a1a")
            set_cell(row, 2, f"{disp_bid_vols[i]:,}", Qt.AlignRight | Qt.AlignVCenter, fg_color="#ff4c4c")
            
        # 스크롤바가 생길 경우 항상 매수/매도가 만나는 중앙으로 강제 고정
        middle_item = self.hoga_table.item(DISPLAY_LEVELS, 1)
        if middle_item:
            self.hoga_table.scrollToItem(middle_item, QAbstractItemView.PositionAtCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    app.setStyleSheet("""
        QWidget { background-color: #1e1e1e; color: #ffffff; }
        QLineEdit, QComboBox, QSpinBox { background-color: #2d2d30; border: 1px solid #555555; color: #ffffff; }
        QDockWidget::title { background-color: #2d2d30; text-align: center; padding: 4px; }
    """)

    kiwoom_api = KiwoomRestAPI(app_key="", app_secret="", is_mock=True)
    login_dialog = LoginDialog(kiwoom_api)

    if login_dialog.exec() == QDialog.Accepted:
        window = HTSMainWindow(api_handler=kiwoom_api) 
        window.fetch_initial_data() 

        window.ws_worker = KiwoomWebSocketWorker(token=kiwoom_api.access_token)
        window.ws_worker.start()

        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()