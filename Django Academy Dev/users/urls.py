from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

# app_name 설정 (템플릿에서 url 태그 쓸 때 필요)
app_name = 'users'

urlpatterns = [
    # 로그인 뷰 (템플릿 위치 지정)
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='/'), name='login'),
    # 로그아웃 뷰 (로그아웃 후 메인('/')으로 이동)
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # 회원가입 뷰
    path('signup/', signup_view, name='signup'),
    # 깃허브 정보 연결뷰
    path('update-github/', update_github_id, name='update_github'),
]