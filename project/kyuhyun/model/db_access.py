from app.model.db_interface import DBInterface

class DB_Access:    # 학생 정보를 가져오기 위해 DB에 접근
    def find_by_std_id(self,std_id):
        db = DBInterface()
        db.connect()

        result = db.fetch_query("""
                   SELECT *
                   FROM students
                   WHERE std_id = ?
               """, std_id)

        db.disconnect()

        return bool(result)

    def find_by_std_name(self, std_name):
        """
        std_name: 찾을 학생 이름
        return: 해당 하는 학생의 정보, 여러개 일 경우 여러개 리턴
        """
        db = DBInterface()
        db.connect()

        result = db.fetch_query("""
            SELECT *
            FROM students
            WHERE name = ?
        """,std_name)

        db.disconnect()

        if len(result) :
            print(result)
            return [
                {'이름': result[i][1], '성별': result[i][2],'주소': result[i][3],'국어': result[i][4], '영어': result[i][5], '수학': result[i][6]}
                for i in range(len(result))
            ]
        else:
            return []
