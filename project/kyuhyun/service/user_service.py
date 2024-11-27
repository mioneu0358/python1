import bcrypt
from flask import session
from app.model.user_access import UserAccess

class UserService:

    def __init__(self):
        self.user_access = UserAccess()

    def registration(self, std_id, user_id, user_pw):
        """
        회원 등록 서비스 함수
        """

        b_user_pw = bytes(user_pw, 'utf-8')
        print(b_user_pw)
        b_hashed_pw = bcrypt.hashpw(password=b_user_pw, salt=bcrypt.gensalt())
        print(b_hashed_pw)
        self.user_access.create_user(std_id,user_id, b_hashed_pw)

    def login(self, user_id, user_pw):
        """
        로그인 서비스 함수
        """

        # 1. id를 통해 user 정보 가져오기
        user_data = self.user_access.find_user(user_id)

        # 2. id 유효성 검사
        # (아이디가 없습니다.)
        if user_data is None:
            return {
                'state': 'fail',
                'msg': '아이디가 없습니다.'
            }

        # 3. pw 유효성 검사
        # (비밀번호를 틀렸습니다.)
        if not bcrypt.checkpw(bytes(user_pw, 'utf-8'), user_data['pw']):
            return {
                'state': 'fail',
                'msg': '비밀번호를 틀렸습니다.'
            }

        # 4. 세션 부여
        session['user'] = user_data  # 쿠키 데이터

        return {'state': 'success'}


    def session_check(self):
        """
        현재 접속자의 세션 유무 확인
        """
        if 'user' in session:
            return {'state': 'success'}
        else:
            return {'state': 'fail'}


    def logout(self):
        """
        현재 접속자 세션 파기
        """
        session.pop('user')

if __name__ == "__main__":
    print(__name__)
    us = UserService()
    us.registration(1,'aaa','abc')