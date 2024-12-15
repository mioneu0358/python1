from app.models.db_interface import DB_interface

class UserAccess:
    """
    회원 정보에 접근하는
    Database Access Object(DAO)
    """

    def create_user(self, user_id, byte_hashed_password):
        """
        새로운 회원을 생성
        """
        db = DB_interface()
        db.connect()

        db.execute_query("""
            INSERT INTO User (user_id, user_pw)
            VALUES ( ?, ?)
        """, user_id, byte_hashed_password)

        db.disconnect()

    def find_user(self, user_id):
        """
        회원 데이터를 찾음
        """
        db = DB_interface()
        db.connect()

        result = db.fetch_query("""
            SELECT user_id,
                   user_pw
            FROM User
            WHERE user_id = ?
        """, user_id)

        db.disconnect()

        # 검색결과 없음
        if len(result) == 0:
            return None

        return {
            'user_id': result[0][0],
            'user_pw': result[0][1]
        }