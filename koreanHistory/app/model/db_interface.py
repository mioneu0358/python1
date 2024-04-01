import sqlite3
from get_data_for_db import *
class DBInterface:
    """
    데이터베이스 연결, 쿼리 실행, 해제를 정의한 DB 인터페이스
    """
    DB_NAME = "KoreanHistory.db"
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        DB에 연결하여 연결객체와 커서를 획득
        """
        self.connection = sqlite3.connect(self.DB_NAME, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """
        DB와의 연결을 해제함
        (해제하지 않을경우 메모리 누수 발생 및 파일 기반
         데이터베이스의 경우 파일 핸들을 반환하지 않아 문제 생길 수 있음)
        """
        self.connection.close()

    def execute_query(self, query, *param):
        """
        입력한 쿼리를 실행함 (결과값 반환 X)
        :param query: Query String
        """
        # print(f"query: {query}")
        # print(f"param: {param}")
        self.cursor.execute(query, param)  # 쿼리를 실행
        self.connection.commit()    # 데이터베이스에 반영

    def fetch_query(self, query, *param):
        """
        입력한 쿼리를 실행함 (결과값 반환 O)
        :param query: Query String
        :return: Tuple[]
        """
        print(f"query: {query}")
        print(f"param: {param}")
        self.cursor.execute(query, param)
        return self.cursor.fetchall()

    
    
# initialize_once 호출 여부
_initialized = False

def initialize_once():
    """
    db_intercace.py 임포트시 딱 한번 실행할 함수(테이블 초기화)
    """
    global _initialized
    if _initialized:
        return
    db = DBInterface()  # DB인터페이스 인스턴스 생성
    db.connect()
    
    # 테이블 생성
    db.execute_query(
        """
        CREATE TABLE  IF NOT EXISTS Goryeo  (
            incident_id	        INTEGER PRIMARY KEY  AUTOINCREMENT ,   -- 사건 ID(기본키, 자동증가)
            king        	    TEXT NOT NULL,                          -- 왕(NULL 비허용) 
            year	            INT NOT NULL,                      -- 사건 연도(NULL 비허용)
            content	            TEXT NOT NULL                           -- 사건 설명(NULL 비허용)
        )
        """ 
    )
    # 생성된 스키마 확인
    # ret = db.fetch_query("SELECT * FROM sqlite_schema")
    # for r in ret:
    #     print(r)
    korean_dynasty_data = get_korean_dynasty()
    # print(korean_dynasty_data)
    for king, values in korean_dynasty_data.items():
        for year, content in values:
            db.execute_query("""
                INSERT INTO Goryeo(king, year, content)
                VALUES(?,?,?)
            """,king, int(year), content )


    # DB 연결 해제
    db.disconnect()
    
    _initialized = True
    
# 초기화 함수 호출
initialize_once()