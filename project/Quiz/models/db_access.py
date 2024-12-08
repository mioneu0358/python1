from models.db_interface import DB_interface

class DB_access:
    def get_quiz_data(self,category):
        db = DB_interface()
        db.connect()
        result = db.fetch_query("""
            SELECT * FROM Quiz WHERE category = ? ORDER BY RANDOM() LIMIT 1;
        """, category)
        db.disconnect()
        if result:
            print("get_quiz_data result: ",result)
            return result[0]
        else:
            print("결과 없음")
            return None

    def get_word_wrong_answer(self, q_id):
        db = DB_interface()
        db.connect()
        result = db.fetch_query("""
            SELECT word FROM Quiz WHERE q_id != ? ORDER BY RANDOM() LIMIT 3;
        """,q_id)

        if result:
            print(f"get_word_wrong_answer: {result}")
            return list(sum(result,start=()))
        else:
            return None

    def get_answer_by_id(self, q_id):
        db = DB_interface()
        db.connect()
        result = db.fetch_query("""
            SELECT * FROM Quiz WHERE q_id = ?
        """, q_id)

        if result:
            print(f"get_answer_by_id result: {result}")
            return result[0]
        else:
            return None
