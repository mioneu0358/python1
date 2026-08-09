from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm  # 폼 이름을 CustomSignupForm으로 가정

def signup_view(request):
    if request.method == "POST":
        # 1. 사용자가 입력한 데이터를 폼에 바인딩
        form = SignupForm(request.POST)
        
        if form.is_valid():
            # 2. 데이터가 유효하면 데이터베이스에 유저 생성 및 저장
            form.save()
            
            # 3. 성공 메시지 등록 (signup.html이나 이동할 페이지에서 띄울 수 있습니다)
            messages.success(request, "회원가입이 성공적으로 완료되었습니다. 로그인해주세요.")
            
            # 4. 회원가입 완료 후 로그인 페이지로 리다이렉트
            # (로그인 URL 패턴 이름이 'login'이라고 가정했습니다. 설정에 맞게 변경하세요)
            return redirect('accounts:login') 
            
        else:
            # 5. 폼 검증 실패 시 (아이디 중복, 비밀번호 불일치 등)
            # 여기서는 아무것도 하지 않아도 form 객체 내부에 에러 내용이 자동으로 담깁니다.
            messages.error(request, "입력 정보를 다시 확인해주세요.")
            
    else:
        # 6. GET 요청일 때는 빈 폼을 생성
        form = SignupForm()
        
    # GET 요청이거나 POST 검증에 실패했을 때 모두 이 row로 도달하여 
    # 에러 정보가 포함되거나 빈 폼이 담긴 signup.html을 렌더링합니다.
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method =='POST':
        posts = request.POST
    else:
        return render(request, 'login.html')