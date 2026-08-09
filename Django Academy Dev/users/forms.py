from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        # 회원가입 시 학생들에게 받을 정보만 명시해 줘
        fields = ('email', 'name', 'school', 'age')