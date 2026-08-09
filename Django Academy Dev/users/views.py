from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignUpForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def signup_view(request):
    # 이미 로그인한 유저가 회원가입 페이지에 오면 메인으로 돌려보냄
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # 가입 성공 시 자동 로그인
            return redirect('/') # 메인 페이지로 이동
    else:
        form = StudentSignUpForm()
        
    return render(request, 'signup.html', {'form': form})


@login_required
@require_POST
def update_github_id(request):
    """학생이 대시보드에서 깃허브 아이디를 연동할 때 호출됨"""
    github_id = request.POST.get('github_id', '').strip()
    
    if github_id:
        request.user.github_username = github_id
        request.user.save()
        
    return redirect('projects:std_dashboard')