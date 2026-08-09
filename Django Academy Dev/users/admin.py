from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# 1. 커스텀 유저 모델에 맞춘 전용 폼(Form) 정의
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name')

# 2. Admin 클래스 설정
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 방금 위에서 만든 커스텀 폼 연결
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    list_display = ('email', 'name', 'is_staff', 'school', 'phone')
    search_fields = ('email', 'name', 'school')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

    # 상세 페이지 (유저 정보 수정 화면) 레이아웃
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('개인 정보', {'fields': ('name', 'age', 'phone')}),
        ('학생 추가 정보', {'fields': ('school', 'address')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요 일정', {'fields': ('last_login',)}),
    )

    # 유저 생성 화면(Add User) 레이아웃
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )