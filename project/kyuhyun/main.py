from flask import Flask, render_template, request, jsonify
from model.db_access import DB_Access
from service.user_service import UserService

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student/search')
def search_student():
    return render_template('search_student.html')

@app.route('/student/register')
def registing_page():
    return render_template('register.html')

@app.route('/student/register', methods=["POST"])
def register():
    print(request.method)
    if request.method == 'POST':
        std_id = request.form.get('std_id')
        db = DB_Access()
        if db.find_by_std_id(std_id):
            user_id = request.form.get('user_id')
            user_pw = request.form.get('user_pw')
            usa = UserService()
            usa.registration(std_id, user_id, user_pw)

            print("회원가입 성공")
            return render_template('home.html')
        else:
            print("없는 학번입니다.")
            return render_template('home.html')
    else:
        return render_template('register.html')


@app.route('/student/check',methods = ['GET'])
def check_student():
    if request.method == 'GET':
        std_name = request.args.get('std_name')
        print(std_name)
        db = DB_Access()
        result = db.find_by_std_name(std_name)
        print(result)
        return render_template('show_info.html',std_infos=result)

if __name__ == "__main__":
    app.run(debug=True)

# TODO: 학생 정보에 info_release라는 이름으로 공개 여부 bool타입으로 정의, True면 성적 공개, False면 성적 공개 x
# 로그인 유무 필요, 로그인시에는 로그인 버튼 대신 로그아웃과 마이페이지 버튼 생성, 마이페이지는

