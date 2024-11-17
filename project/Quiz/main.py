from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 데이터 (A=1, B=2, ..., Z=26)
data = {chr(i): i - 64 for i in range(65, 91)}  # A-Z 알파벳 데이터

@app.route('/')
def index():
    return render_template('home.html')


# 문제 출제 라우트
@app.route('/solve', methods=['GET'])
def quiz():
    import random
    question = random.choice(list(data.keys()))  # 랜덤으로 알파벳 선택
    return render_template('quizquiz.html', q=question)  # HTML 파일 이름을 quiz_timer.html로 가정

# 정답 제출 라우트
@app.route('/check/<question_id>', methods=['POST'])
def check_answer(question_id):
    user_answer = request.form.get('answer')  # 사용자가 입력한 값
    correct_answer = data.get(question_id.upper())  # 데이터에서 정답 가져오기
    
    if user_answer and int(user_answer) == correct_answer:  # 정답 확인
        return render_template('correct.html')  # 정답 시
    else:
        return render_template('fail.html', answer=correct_answer)  # 오답 시 정답 출력

if __name__ == '__main__':
    app.run(debug=True)


# TODO: db를 만들기 위해 단어 딕셔너리 만들기
# {카테고리: {단어: 내용, ...}, ...} 형태로 저장
# 저장된 데이터 DB에 할당하기
# 나중에는 DB서버를 따로 만들어 불러오는 방식으로 사용

