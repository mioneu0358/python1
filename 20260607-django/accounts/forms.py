from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm
from django import forms

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
            model = User
            # 회원가입 폼에 노출할 필드만 지정합니다. (role, participated_projects 제외)
            fields = ['username', ] 
            labels = {
                 'username': '아이디',
            }
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # UserCreationForm이 내부적으로 만드는 필드에 접근하여 label을 덮어씌웁니다.
        self.fields['password1'].label = '비밀번호'            
        self.fields['password2'].label = '비밀번호 확인'


class LoginForm(Form):
     username = forms.CharField(
          max_length=150,
          widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'})
     )