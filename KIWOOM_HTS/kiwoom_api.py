import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, json

class KiwoomRestAPI:
    def __init__(self, app_key, app_secret, is_mock=True):
        self.app_key = app_key
        self.app_secret = app_secret
        # 모의투자 및 실투자 도메인 분리
        self.base_url = "https://mockapi.kiwoom.com" if is_mock else "https://api.kiwoom.com"
        
        self.access_token = None
        self.expires_dt = None

    def _is_token_valid(self):
        if not self.access_token or not self.expires_dt:
            return False
        # 만료 5분 전에는 미리 갱신하도록 처리
        return datetime.now() < (self.expires_dt - timedelta(minutes=5))

    def issue_token(self):
        """Oauth 2.0 기반 토큰 발급 및 갱신"""
        url = f"{self.base_url}/oauth2/token"
        headers = {"content-type": 'application/json;charset=UTF-8'}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "secretkey": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            print(data)
            self.access_token = data.get("token")
            expires_in = data.get("expires_dt") # 기본 24시간
            self.expires_dt = datetime.strptime(expires_in, "%Y%m%d%H%M%S")
            return True, "토큰 발급 성공"
        return False, f"토큰 발급 실패: {response.text}"

    def get_headers(self, api_id, cont_yn='N', next_key=''):
        """API 요청에 필요한 공통 헤더 (API 명세 반영)"""
        if not self._is_token_valid():
            self.issue_token()
            
        return {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.access_token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': api_id
        }

    def get_account_numbers(self, cont_yn='N', next_key=''):
        """계좌번호조회 (TR: ka00001)"""
        endpoint = '/api/dostk/acnt'
        url = self.base_url + endpoint
        
        # 헤더에 api-id 'ka00001' 지정
        headers = self.get_headers(api_id='ka00001', cont_yn=cont_yn, next_key=next_key)
        
        # API 명세서에 따른 빈 파라미터 전달
        params = {}        
        response = requests.post(url, headers=headers, json=params)        

        return response.json()

    def get_account_balance(self, qry_tp='1', dmst_stex_tp='KRX', cont_yn='N', next_key=''):
        """계좌평가잔고내역요청 (TR: kt00018)"""
        endpoint = '/api/dostk/acnt'
        url = self.base_url + endpoint
        
        # 헤더에 api-id 'kt00018' 지정
        headers = self.get_headers(api_id='kt00018', cont_yn=cont_yn, next_key=next_key)
        
        # API 명세서에 따른 필수 파라미터 전달
        params = {
            'qry_tp': qry_tp,          # 조회구분 1:합산, 2:개별
            'dmst_stex_tp': dmst_stex_tp # 국내거래소구분 KRX:한국거래소, NXT:넥스트트레이드
        }
        
        response = requests.post(url, headers=headers, json=params)
        
        return response.json()

    def get_daily_realized_pl(self, strt_dt, end_dt, cont_yn='N', next_key=''):
        """일자별실현손익요청 (TR: ka10074)"""
        endpoint = '/api/dostk/acnt'
        url = self.base_url + endpoint
        
        headers = self.get_headers(api_id='ka10074', cont_yn=cont_yn, next_key=next_key)
        
        params = {
            'strt_dt': strt_dt,
            'end_dt': end_dt
        }
        
        response = requests.post(url, headers=headers, json=params)
        print(response.json())
        return response.json()

    def get_stock_info_list(self, mrkt_tp='0', cont_yn='N', next_key=''):
        """종목정보 리스트 요청 (TR: ka10099)"""
        endpoint = '/api/dostk/stkinfo'
        url = self.base_url + endpoint
        
        headers = self.get_headers(api_id='ka10099', cont_yn=cont_yn, next_key=next_key)
        params = {'mrkt_tp': mrkt_tp}
        
        response = requests.post(url, headers=headers, json=params)
        return response.json()

    def get_stock_hoga(self, stk_cd, cont_yn='N', next_key=''):
        """주식호가요청 (TR: ka10004)"""
        endpoint = '/api/dostk/mrkcond'
        url = self.base_url + endpoint
        
        headers = self.get_headers(api_id='ka10004', cont_yn=cont_yn, next_key=next_key)
        params = {'stk_cd': stk_cd}
        
        response = requests.post(url, headers=headers, json=params)
        return response.json()        


    def get_chart_data(self, stk_cd, timeframe="일봉", base_dt=None, cont_yn='N', next_key=''):
        """요청된 주기에 맞춰 틱/분/일/주/월/년 차트 TR을 동적으로 호출합니다."""
        if base_dt is None:
            base_dt = datetime.now().strftime("%Y%m%d")

        endpoint = '/api/dostk/chart'
        url = self.base_url + endpoint
        
        # 콤보박스 선택값에 따른 API ID 및 파라미터 매핑
        params = {'stk_cd': stk_cd, 'upd_stkpc_tp': '1'} 

        if timeframe == "일봉":
            api_id = 'ka10081'
            params['base_dt'] = base_dt
        elif timeframe == "주봉":
            api_id = 'ka10082'
            params['base_dt'] = base_dt
        elif "분봉" in timeframe:
            api_id = 'ka10080'
            scope = timeframe.replace("분봉(", "").replace("분)", "") # 예: "분봉(3분)" -> "3"
            params['base_dt'] = base_dt
            params['tic_scope'] = scope
        elif timeframe == "틱(10틱)":
            api_id = 'ka10079'
            params['tic_scope'] = '10'
        else:
            api_id = 'ka10081' # 기본값
            params['base_dt'] = base_dt

        headers = self.get_headers(api_id=api_id, cont_yn=cont_yn, next_key=next_key)
        response = requests.post(url, headers=headers, json=params)
        
        # 워커에서 파싱할 때 어떤 데이터 키를 찾아야 하는지 알 수 있도록 api_id도 함께 반환
        return response.json(), api_id
    
if __name__ == "__main__":
    load_dotenv()
    appkey = os.getenv("APPKEY")
    secretkey = os.getenv("APPSECRET")
    
    # 모의투자로 테스트 (실전투자시 is_mock=False 로 변경)
    k = KiwoomRestAPI(appkey, secretkey, is_mock=True)
    
    success, msg = k.issue_token()
    print("=== 토큰 발급 결과 ===")
    print(msg)
    
    if success:
        print("\n=== 1. 계좌번호 조회 테스트 (ka00001) ===")
        print(k.get_account_numbers())
        
        print("\n=== 2. 계좌평가잔고 조회 테스트 (kt00018) ===")
        print(k.get_account_balance())