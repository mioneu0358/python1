from app.model.db_interface import DBInterface

class DBAccess:
    """
    게시판에 관련된 데이터에 접근하는 DataBase Access Object(DAO)
    """
    
    def find_all_incident():
        """
        모든 사건 반환
        """
        db = DBInterface
        db.connect()
        
        result = db.fetch_query(
        """
        SELECT incident_title,
               date,
               content,
               FROM KoreanHistory
               ORDER BY date
        """
        )
        db.disconnect()
        
        if len(result) == 0:
            return []
        
        for i in range(len(result)):
            result[i] = {
                'incident_title' : result[i][0],
                'date'           : result[i][1],
                'content'        : result[i][2]
            }
        return result
    
    def find_incident_by_title(self, title):
        """
        title값을 통해 카테고리를 찾는다.    
        """
        db = DBInterface()
        db.connect()
        
        result = db.fetch_query(
        """
        SELECT incident_title,
               date,
               content,
        FROM KoreanHistory
        WHERE incident_title = ?
        ORDER BY date
        """, title)
        
        db.disconnect()
        
        if len(result) == 0:
            return []
        
        for i in range(len(result)):
            result[i] = {
                'incident_title' : result[i][0],
                'date'           : result[i][1],
                'content'        : result[i][2]
            }
        return result
    
    def find_incident_by_date(self, date):
        """
        title값을 통해 카테고리를 찾는다.    
        """
        db = DBInterface()
        db.connect()
        
        result = db.fetch_query(
        """
        SELECT incident_title,
               date,
               content,
        FROM KoreanHistory
        WHERE date = ?
        ORDER BY date
        """, date)
        
        db.disconnect()
        
        if len(result) == 0:
            return []
        
        for i in range(len(result)):
            result[i] = {
                'incident_title' : result[i][0],
                'date'           : result[i][1],
                'content'        : result[i][2]
            }
        return result