from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """학생(일반 유저) 생성 시 사용되는 메서드"""
        if not email:
            raise ValueError('이메일 주소는 필수입니다.')
        
        email = self.normalize_email(email)
        # 일반 유저는 기본적으로 학생으로 간주
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """선생님(최고 관리자) 생성 시 사용되는 메서드 (createsuperuser 명령어)"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # 관리자는 주소나 학교 정보가 필요 없으므로 빈 값 처리 가능
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser는 is_staff=True 여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser는 is_superuser=True 여야 합니다.')

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # 공통 필수 필드 (선생님 & 학생)
    email = models.EmailField(unique=True, verbose_name="이메일")
    name = models.CharField(max_length=50, verbose_name="이름")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="나이")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="전화번호")
    github_username = models.CharField(max_length=50, null=True, blank=True, verbose_name="GitHub 아이디")
    # 학생 전용 필드 (선생님 계정일 땐 비워둠)
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="주소")
    school = models.CharField(max_length=100, null=True, blank=True, verbose_name="학교")

    # 권한 및 상태 필드 (Django 필수)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # True면 Admin 페이지 접근 가능 (선생님)

    objects = CustomUserManager()

    # 이메일을 로그인 ID로 사용
    USERNAME_FIELD = 'email'
    
    # createsuperuser 실행 시 터미널에서 입력받을 추가 필수 필드
    # (email과 password는 기본으로 받으므로 제외)
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"