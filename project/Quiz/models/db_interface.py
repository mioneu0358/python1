from models.download_korean import get_korean
import sqlite3
import os
DB_name = "test.db"

class DB_interface:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """DB연결 함수"""
        self.connection = sqlite3.connect(DB_name,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """DB연결 해제 함수"""
        self.connection.close()

    def execute_query(self,query,*params):
        """query 실행함수(결과값 X)"""
        self.cursor.execute(query,params)
        self.connection.commit()

    def fetch_query(self,query,*params):
        """query 실행함수(결과값 O)"""
        self.cursor.execute(query,params)
        return self.cursor.fetchall()



def initialize_db():
    # 코드 실행중에 한번만 실행되도록 만든다.
    print(os.path.isfile(DB_name))
    if os.path.isfile(DB_name):
       return
    # DB가 있던 없던, DB를 초기화하는 작업을 해준다.
    # DB가 없다면 해당 DB의 테이블 생성
    # 테이블: Korean
    # column명: Q_id      PRIMARY KEY INTEGER AUTO INCREAEMENT 기본키, 정수타입, 자동증가
    #           word      TEXT, NOT NULL                        문자타입, 값을 무조건 할당
    #           word_exp  TEXT, NOT NULL                        문자타입, 값을 무조건 할당

    # db연결, db에 테이블이 없는 경우에 생성

    db = DB_interface()
    db.connect()

    db.execute_query("""
        CREATE TABLE IF NOT EXISTS Quiz (
            Q_id       INTEGER PRIMARY KEY AUTOINCREMENT, -- 문제 번호
            category   TEXT NOT NULL,                     -- 문제 유형
            word       TEXT NOT NULL,                     -- 단어
            word_exp   TEXT NOT NULL                      -- 단어 설명
        )
    """)
    print("한글 단어 가져오기 -----------------------------------------------------------")
    korean_data = get_korean()
    print(korean_data)

    for word,word_exp in korean_data.items():
        db.execute_query("""
            INSERT INTO Quiz (category, word, word_exp)
            VALUES ("korean", ?, ?)
        """, word, word_exp)

    ret = db.fetch_query("SELECT * FROM Quiz")
    for r in ret:
        print(r)

    # DB 연결 해제
    db.disconnect()

initialize_db()