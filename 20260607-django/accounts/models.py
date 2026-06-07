from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# python manage createsuperuser 명령어로 만들 수퍼계정 manager
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # createsuperuser 실행 시 자동으로 role을 'owner'로 덮어씌움
        extra_fields.setdefault('role', 'owner')
        
        # 만약 is_staff나 is_superuser 권한이 False로 들어오면 강제 설정 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # 기존 UserManager의 create_superuser 로직 그대로 실행
        return super().create_superuser(username, email, password, **extra_fields)
    


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        OWNER = 'owner', '사이트 주인'
        COLLEAGUE = 'colleague', '동료'
        REGULAR = 'regular', '일반 회원'

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.REGULAR,
        verbose_name='사용자 역할'
    )

    participated_projects = models.ManyToManyField(
        'projects.Project',                         # 연결할 테이블
        blank=True,
        related_name='participants',                # related_name: 역참조 이름
        verbose_name='참여한 프로젝트'               #
    )

    # CustomUserManager를 이용하여 사용자 생성을 진행한다고 명시
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"