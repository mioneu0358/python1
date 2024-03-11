from app.model.db_access import DBAccess

class DBService:
    """
    게시판 관련 비즈니스 로직을 처리하는 서비스 클래스
    """
    
    def __init__(self):
        self.db_access = DBAccess()
        
    def get_all_title(self):
        """
        모든 사건들을 불러온다.
        """
        return self.db_access.find_all_incident()
    
