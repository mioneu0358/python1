from app.model.db_access import DBAccess

class DBService:
    """
    게시판 관련 비즈니스 로직을 처리하는 서비스 클래스
    """
    
    def __init__(self):
        self.db_access = DBAccess()
        
    # def get_all_title(self):
    #     """
    #     모든 사건들을 불러온다.
    #     """
    #     return self.db_access.find_all_incident()
    
    def get_incident(self,king,year,content):
        """
        조건에 해당하는 사건을 불러온다.
        """
        return self.db_access.find_incident_by_category(king,year,content)