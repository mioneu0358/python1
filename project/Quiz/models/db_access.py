from db_interface import DB_interface

class DB_access:
    def get_quiz_data(self):
        db = DB_interface()
        db.connect()
        result = db.fetch_query("""
            SELECT * FROM Korean LIMIT 1;
        """)
        db.disconnect()
        if result:
            print("result: ",result)
        else:
            print("결과 없음")

db = DB_access()
print(db.get_quiz_data())
