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
        
        # 응답 상태 확인 및 출력
        print('Code:', response.status_code)
        print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
        print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))
        
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
        
        # 응답 상태 확인 및 출력
        print('Code:', response.status_code)
        print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
        print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))
        
        return response.json()

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