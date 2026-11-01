# Workers.py
import json
from datetime import datetime
from queue import Queue
from PySide6.QtCore import QThread, Signal



class SystemInitWorker(QThread):
    # (성공여부, 잔고데이터, 종목리스트) 반환
    finished = Signal(bool, dict, list)

    def __init__(self, api_handler):
        super().__init__()
        self.api = api_handler

    def run(self):
        try:
            # 1. 잔고 및 실현손익 조회 (기존 로직)
            balance_result = self.api.get_account_balance()
            today_str = datetime.now().strftime("%Y%m%d")
            realized_result = self.api.get_daily_realized_pl(today_str, today_str)
            
            if balance_result.get("return_code") == 0:
                balance_result["rlzt_pl"] = realized_result.get("rlzt_pl", "0") if realized_result.get("return_code") == 0 else "0"
            
            # 2. 종목 마스터 데이터 수집 (코스피: '0', 코스닥: '10')
            kospi_res = self.api.get_stock_info_list(mrkt_tp='0')
            kosdaq_res = self.api.get_stock_info_list(mrkt_tp='10')
            # print(f"kosdaq_res: {kosdaq_res}")

            master_list = []
            # 응답받은 두 시장의 리스트를 순회하며 "종목명 (종목코드)" 형태의 문자열 리스트 생성
            for res in (kospi_res, kosdaq_res):
                if res.get("return_code") == 0:
                    for stock in res.get("list", []):
                        # 예: "삼성전자 (005930)"
                        master_list.append(f"{stock['name']} ({stock['code']})")
            # print(f"SystemInitWorker - master_list:{master_list}")
            self.finished.emit(True, balance_result, master_list)
                
        except Exception as e:
            self.finished.emit(False, {"return_msg": str(e)}, [])


class ChartDataWorker(QThread):
    # (성공여부, 종목코드, 차트데이터리스트) 반환
    finished = Signal(bool, str, list)

    def __init__(self, api_handler, stock_code, timeframe):
        super().__init__()
        self.api = api_handler
        self.stock_code = stock_code
        self.timeframe = timeframe # "일봉", "분봉(1분)" 등

    def run(self):
        try:
            # TODO: 키움 API 차트 데이터 조회 TR 호출 (예: opt10081 등)
            # chart_result = self.api.get_chart_data(self.stock_code, self.timeframe)
            
            # if chart_result.get("return_code") == 0:
            #     candle_list = chart_result.get("list", [])
            #     self.finished.emit(True, self.stock_code, candle_list)
            # else:
            #     self.finished.emit(False, self.stock_code, [])
            
            # 임시 더미 데이터 발사
            self.finished.emit(True, self.stock_code, []) 
        except Exception as e:
            self.finished.emit(False, self.stock_code, [])

import json

# 스레드 간 공유될 실시간 호가 버퍼 (가장 최신 호가 상태만 유지)
realtime_hoga_buffer = {}

class KiwoomWebSocketWorker(QThread):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.current_stk = ""
        self.is_running = True

    def subscribe(self, stock_code):
        """UI 스레드에서 새 종목 검색 시 호출하여 구독 대상 변경"""
        self.current_stk = stock_code
        # TODO: 키움 서버로 '기존 구독 해지 및 새 종목 구독' JSON 패킷 전송 로직 추가

    def run(self):
        # TODO: 키움 웹소켓 URL 연결 (websocket-client 라이브러리 활용)
        while self.is_running:
            # 서버에서 받은 수신 데이터라고 가정 (Raw JSON)
            # raw_data = ws.recv() 
            # parsed = json.loads(raw_data)
            
            # realtime_hoga_buffer[parsed['stk_cd']] = parsed
            
            self.msleep(10) # 임시 대기


class HogaDataWorker(QThread):
    finished = Signal(bool, str, dict)

    def __init__(self, api_handler, stock_code):
        super().__init__()
        self.api = api_handler
        self.stock_code = stock_code

    def run(self):
        try:
            result = self.api.get_stock_hoga(self.stock_code)
            
            if result.get("return_code") == 0:
                ask_prices, ask_vols = [], []
                bid_prices, bid_vols = [], []
                
                # --- 매도 호가 (10호가 -> 1호가 순서로 쌓기 : 가장 높은 가격이 위로 가도록) ---
                for i in range(10, 1, -1):
                    # 호가에 포함된 부호(+, -)를 제거하기 위해 abs() 사용
                    ask_prices.append(abs(int(result.get(f"sel_{i}th_pre_bid", 0))))
                    ask_vols.append(int(result.get(f"sel_{i}th_pre_req", 0)))
                
                # 매도 1호가 (키 이름이 다름)
                ask_prices.append(abs(int(result.get("sel_fpr_bid", 0))))
                ask_vols.append(int(result.get("sel_fpr_req", 0)))
                
                # --- 매수 호가 (1호가 -> 10호가 순서로 쌓기 : 가장 높은 가격이 위로 가도록) ---
                # 매수 1호가
                bid_prices.append(abs(int(result.get("buy_fpr_bid", 0))))
                bid_vols.append(int(result.get("buy_fpr_req", 0)))
                
                for i in range(2, 11):
                    bid_prices.append(abs(int(result.get(f"buy_{i}th_pre_bid", 0))))
                    bid_vols.append(int(result.get(f"buy_{i}th_pre_req", 0)))

                parsed_data = {
                    "ask_prices": ask_prices,
                    "ask_vols": ask_vols,
                    "bid_prices": bid_prices,
                    "bid_vols": bid_vols
                }
                self.finished.emit(True, self.stock_code, parsed_data)
            else:
                self.finished.emit(False, self.stock_code, {})
                
        except Exception as e:
            self.finished.emit(False, self.stock_code, {})

class BalanceDataWorker(QThread):
    """잔고 및 실현손익만 빠르고 가볍게 가져오는 전용 워커"""
    finished = Signal(bool, dict) # 성공여부, 잔고데이터 반환

    def __init__(self, api_handler):
        super().__init__()
        self.api = api_handler

    def run(self):
        try:
            balance_result = self.api.get_account_balance()
            today_str = datetime.now().strftime("%Y%m%d")
            realized_result = self.api.get_daily_realized_pl(today_str, today_str)
            
            if balance_result.get("return_code") == 0:
                balance_result["rlzt_pl"] = realized_result.get("rlzt_pl", "0") if realized_result.get("return_code") == 0 else "0"
                self.finished.emit(True, balance_result)
            else:
                self.finished.emit(False, balance_result)
                
        except Exception as e:
            self.finished.emit(False, {"return_msg": str(e)})

class ChartDataWorker(QThread):
    finished = Signal(bool, str, list) # 성공여부, 종목코드, 차트데이터 배열

    def __init__(self, api_handler, stock_code, timeframe):
        super().__init__()
        self.api = api_handler
        self.stock_code = stock_code
        self.timeframe = timeframe 

    def run(self):
        try:
            result, api_id = self.api.get_chart_data(self.stock_code, self.timeframe)
            
            if result.get("return_code") == 0:
                # 응답 형태에 맞춘 데이터 키 맵핑[cite: 8]
                key_map = {
                    'ka10079': 'stk_tic_chart_qry',
                    'ka10080': 'stk_min_pole_chart_qry',
                    'ka10081': 'stk_dt_pole_chart_qry',
                    'ka10082': 'stk_stk_pole_chart_qry'
                }
                
                target_key = key_map.get(api_id, 'stk_dt_pole_chart_qry')
                raw_list = result.get(target_key, [])
                
                parsed_data = []
                for t, item in enumerate(raw_list):
                    o = abs(int(item.get("open_pric", 0)))
                    h = abs(int(item.get("high_pric", 0)))
                    l = abs(int(item.get("low_pric", 0)))
                    c = abs(int(item.get("cur_prc", 0)))
                    v = int(item.get("trde_qty", 0))
                    
                    # 일봉은 'dt', 분봉/틱봉은 'cntr_tm'을 키로 사용함
                    time_str = item.get("dt", item.get("cntr_tm", ""))
                    
                    parsed_data.append((t, o, h, l, c, v, time_str)) # time_str 추가!
                
                parsed_data.reverse()
                # 인덱스를 0부터 다시 정렬하며 time_str도 포함하여 반환
                reindexed_data = [(i, row[1], row[2], row[3], row[4], row[5], row[6]) for i, row in enumerate(parsed_data)]
                
                self.finished.emit(True, self.stock_code, reindexed_data)
            else:
                self.finished.emit(False, self.stock_code, [])
        except Exception as e:
            self.finished.emit(False, self.stock_code, [])