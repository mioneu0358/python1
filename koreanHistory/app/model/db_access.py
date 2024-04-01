from app.model.db_interface import DBInterface

class DBAccess:
    """
    게시판에 관련된 데이터에 접근하는 DataBase Access Object(DAO)
    """
    def find_incident_by_category(self,king,year,content):
        """_
        조건을 통해 데이터를 찾는다.
        """
        db = DBInterface()
        db.connect()
        if year != 0:
            result = db.fetch_query("""
            SELECT DISTINCT king, year, content
            FROM Goryeo
            WHERE king like ? AND
                  year = ? AND
                  content like ?
            ORDER BY year;
            """, king,year, content)
            print(f"result: {result}")
        else:                                                    #  연도가 정해져 있지 않다면 모든 연도에서 검색
            result = db.fetch_query("""
                        SELECT DISTINCT king, year, content
                        FROM Goryeo
                        WHERE king like ? AND
                              year >= ? AND
                              content like ?
                        ORDER BY year;
                        """, king, year, content)
            print(f"result: {result}")

        db.disconnect()

        if len(result) == 0:
            return []

        for i in range(len(result)):
            result[i] = {
                'king': result[i][0],
                'year': str(result[i][1]) + '년',
                'content': result[i][2]
            }
        return result

