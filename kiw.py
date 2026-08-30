import requests
import json, os
from dotenv import load_dotenv

load_dotenv()

class MYKIWOOM:
    def __init__(self):
        self.APIKEY = os.getenv("APPKEY")
        self.SECRETKEY = os.getenv("APPSECRET")
        print(self.APIKEY)
        print(self.SECRETKEY)
        self.host = 'https://mockapi.kiwoom.com' # 모의투자
        self.TOKEN = ''
        self.EXPIRES_DT = ''
        self.ACC_NUM = ''
        self._get_token_info()
        self._get_account_number()
        self.get_account_info()
    def _get_token_info(self,):
        endpoint = '/oauth2/token'
        url =  self.host + endpoint
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        }
        data = {
            'grant_type': 'client_credentials',  # grant_type
            'appkey': self.APIKEY,  # 앱키
            'secretkey': self.SECRETKEY,  # 시크릿키
        }

        response = requests.post(url, headers=headers, json=data).json()
        print(response)
        self.TOKEN = response['token']
        self.EXPIRES_DT = response['expires_dt']
        print(self.TOKEN)
        print(self.EXPIRES_DT)


    # 계좌번호조회
    def _get_account_number(self, data={}, cont_yn='N', next_key=''):
        endpoint = '/api/dostk/acnt'
        url =  self.host + endpoint

        # 2. header 데이터
        headers = {
            'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
            'authorization': f'Bearer {self.TOKEN}', # 접근토큰
            'cont-yn': cont_yn, # 연속조회여부
            'next-key': next_key, # 연속조회키
            'api-id': 'ka00001' # TR명
        }

        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data).json()
        self.ACC_NUM = response['acctNo']

        print(self.ACC_NUM)



    # 예수금상세현황요청
    def get_account_info(self, data={}, cont_yn='N', next_key=''):
        # 1. 요청할 API URL
        endpoint = '/api/dostk/acnt'
        url =  self.host + endpoint
        vars = {'tot_pur_amt': '총매입금액', 'tot_evlt_amt': '총평가금액', 'tot_evlt_pl': '총평가손익금액', 'tot_prft_rt': '총수익률(%)', 'prsm_dpst_aset_amt': '추정예탁자산', 'tot_loan_amt':'총대출금', 'tot_crd_loan_amt': '총융자금액', 'tot_crd_ls_amt': '총대주금액', 'acnt_evlt_remn_indv_tot': '계좌평가잔고개별합산', 'stk_cd': '종목번호', 'stk_nm': '종목명', 'evltv_prft': '평가손익', 'prft_rt': '수익률(%)', 'pur_pric': '매입가', 'pred_close_pric': '전일종가', 'rmnd_qty': '보유수량', 'trde_able_qty': '매매가능수량', 'cur_prc': '현재가', 'pred_buyq': '전일매수수량', 'pred_sellq': '전일매도수량', 'tdy_buyq': '금일매수수량', 'tdy_sellq': '금일매도수량', 'pur_amt': '매입금액', 'pur_cmsn': '매입수수료', 'evlt_amt': '평가금액', 'sell_cmsn': '평가수수료', 'tax': '세금', 'sum_cmsn': '수수료합', 'poss_rt': '보유비중(%)', 'crd_tp': '신용구분', 'crd_tp_nm': '신용구분명', 'crd_loan_dt': '대출일'}
        # 2. header 데이터
        headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {self.TOKEN}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'kt00018' # TR명
        }
        data = {
		'qry_tp': '1', # 조회구분 1:합산, 2:개별
		'dmst_stex_tp': 'KRX' # 국내거래소구분 KRX:한국거래소,NXT:넥스트트레이드
        }


        # 3. http POST 요청
        response = requests.post(url, headers=headers, json=data).json()
        print(response)
        for key,val in vars.items():
            if key in response:
                v = response[key]
                if type(v) != str: continue
                print(f"{val}: {float(response[key]):,}")



import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from testUI import Ui_Dialog  # 변환된 UI 모듈
from main import MYKIWOOM
import time

class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # UI 설정
        self.show()
        self.testbtn1.clicked.connect(self.func1)
        self.testbtn2.clicked.connect(self.func2)
    
    def func1(self):
        time.sleep(5)

    def func2(self):
        self.testlabel.setText(k.ACC_NUM)

if __name__ == "__main__":
    k = MYKIWOOM()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

# 자동매매 로직
