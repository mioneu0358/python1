from flask import Flask, render_template, request, redirect, url_for
from models.db_access import DB_access
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

# 문제 출제 라우트
@app.route('/solve/<category>', methods=['GET'])
def quiz(category):
    db = DB_access()
    q_id,q_category, word,word_exp = db.get_quiz_data(category)
    wrong_words = db.get_word_wrong_answer(q_id)
    print(f"q_id: {q_id}, word: {word}, word_exp: {word_exp}")
    print(f"wrong_words : {wrong_words}")
    example = [word, *wrong_words]
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
            return render_template('correct.html', category = category)  # 정답 시
        else:
            return render_template('fail.html', answer=word, category=category)  # 오답 시 정답 출력

if __name__ == '__main__':
    app.run(debug=True)

