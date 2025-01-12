from flask import Flask, render_template, request, redirect, url_for
from models.db_access import DB_access
from service.user_service import UserService
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

# TODO: 세션 체크
@app.route('/')
def index():
    user_data = UserService.get_user()
    print(f"/ user_data: {user_data}")
    # if user_data:
    #     return render_template('home.html', user_data = user_data)
    # else:

    return render_template('home.html')

@app.route('/login', methods=["POST"])
def login():
    """
    입력한 user_id와 user_pw를 불러와 db에서 확인후 session에 user정보 추가
    :return:
    """
    user_id = request.form.get('user_id')
    user_pw = request.form.get('user_pw')

    user_service = UserService()
    result = user_service.login(user_id, user_pw)

    if result['state'] == 'success':
        return render_template('home.html', login_status='success')
    else:
        return render_template('home.html', login_status='fail', error_msg=result['msg'])

@app.route('/logout', methods=['POST'])
def logout():
    """
    세션에서 유저 정보 제거 후 홈 화면으로 전송
    """
    user_service = UserService()
    user_service.logout()
    return redirect('/')


@app.route('/register')
def registing_page():
    """
    회원가입 페이지 보여주기
    """
    return render_template('register.html')

@app.route('/register', methods=["POST"])
def register():
    """
    회원가입 처리 라우터
    """
    user_id = request.form.get('user_id')
    user_pw = request.form.get('user_pw')

    # 필수 값 검증
    if not user_id or not user_pw:
        return render_template(
            'register.html',
            error_msg="모든 필드를 입력해주세요."
        )
    user_service = UserService()
    try:
        user_service.registration(user_id, user_pw)
        return render_template(
            'home.html',
            success_msg="회원가입이 성공적으로 완료되었습니다!"
        )
    except Exception as e:
        # 중복된 ID 등의 예외 처리
        # print(str(e).strip() == "UNIQUE constraint failed: User.std_id")
        if str(e) == "UNIQUE constraint failed: User.user_id":
            return render_template('register.html',
               error_msg="중복된 아이디 입니다. 다른 아이디를 사용해주세요.")
        return render_template(
            'register.html',
            error_msg=f"회원가입 중 오류가 발생했습니다: {e}"
        )

# 문제 출제 라우트
@app.route('/solve/<category>', methods=['GET'])
def quiz(category):
    db = DB_access()
    # session에 들어있는 유저 정보의 푼 문제 수의 값 증가
    UserService.total_cnt_plus()
    user_data = UserService.get_user()
    print(f"solve/{category} user_data: {user_data}")
    q_id,q_category, word,word_exp = db.get_quiz_data(category)
    wrong_words = db.get_word_wrong_answer(q_id,category)
    print(f"q_id: {q_id}, word: {word}, word_exp: {word_exp}")
    print(f"wrong_words : {wrong_words}")
    example = list({word, *wrong_words})
    return render_template('quizquiz.html', word_exp=word_exp, q_id=q_id, example = example)  # HTML 파일 이름을 quiz_timer.html로 가정

# 정답 제출 라우트
@app.route('/check/<q_id>', methods=['POST'])
def check_answer(q_id):
    user_answer = request.form.get('answer')  # 사용자가 입력한 값
    db = DB_access()
    result = db.get_answer_by_id(q_id)
    if result:
        q_id, category, word, word_exp = result
        print(f"correct_answer: {word}")
        if user_answer == word:  # 정답 확인
            # session에 들어있는 유저정보의 맞춘개수 증가
            UserService.correct_cnt_plus()
            return render_template('correct.html', category = category, word=word, word_exp = word_exp)  # 정답 시
        else:
            return render_template('fail.html', answer=word,exp = word_exp, category=category, wrong_answer = user_answer)  # 오답 시 정답 출력

if __name__ == '__main__':
    app.run(debug=True)

