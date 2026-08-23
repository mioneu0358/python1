from django.db import models
from django.conf import settings

class DailyJournal(models.Model):
    # 어떤 학생의 일지인지 연결
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='journals')
    
    date = models.DateField(verbose_name="수업 날짜")
    title = models.CharField(max_length=200, verbose_name="오늘의 핵심 요약")
    content = models.TextField(verbose_name="상세 노트 및 코드 (마크다운)")
    
    # 깃허브 커밋 주소를 수동으로 넣거나 API로 자동 매핑할 때 사용
    github_commit_url = models.URLField(null=True, blank=True, verbose_name="관련 커밋 URL")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.date}] {self.student.name} - {self.title}"

class StudyClass(models.Model):
    """학생들이 소속된 반 (예: 고급 파이썬 1반)"""
    name = models.CharField(max_length=100, verbose_name="반 이름")
    description = models.TextField(blank=True, null=True, verbose_name="반 설명")
    
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="팀/그룹 이름")
    is_official = models.BooleanField(default=False, verbose_name="공식 반 여부") # 선생님이 만든 반이면 True
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="생성자")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='my_teams', verbose_name="소속 팀원")
    
    def __str__(self):
        return self.name

# ==========================================
# 1. 프로젝트 코어 영역 (권한 및 메타데이터)
# ==========================================
class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="프로젝트 명")
    description = models.TextField(blank=True, null=True, verbose_name="프로젝트 개요")
    start_date = models.DateField(null=True, blank=True, verbose_name="시작일")
    end_date = models.DateField(null=True, blank=True, verbose_name="종료일")
    
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='led_projects', verbose_name="팀장")
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participating_projects', verbose_name="참여 인원")
    
    # 변경된 부분: study_class 대신 team을 참조합니다.
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects', verbose_name="소속 팀/그룹")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): return self.title
    
    @property
    def project_type(self):
        """참여 인원이 2명 이상이면 팀 프로젝트, 1명이면 개인 프로젝트로 구분"""
        return "팀 프로젝트" if self.participants.count() > 1 else "개인 프로젝트"

# ==========================================
# 2. 프로젝트 단계 및 체크리스트 (진행 관리)
# ==========================================
class ProjectStage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100, verbose_name="단계명 (예: 기획, DB설계)")
    order = models.PositiveIntegerField(default=0, verbose_name="순서")
    
    # 💡 새롭게 추가된 기간 필드
    start_date = models.DateField(null=True, blank=True, verbose_name="단계 시작일")
    end_date = models.DateField(null=True, blank=True, verbose_name="단계 종료일")
    
    class Meta:
        ordering = ['order']
        
    def __str__(self): return f"{self.project.title} - {self.name}"

class Checklist(models.Model):
    stage = models.ForeignKey(ProjectStage, on_delete=models.CASCADE, related_name='checklists')
    content = models.CharField(max_length=255, verbose_name="할 일")
    is_completed = models.BooleanField(default=False, verbose_name="완료 여부")
    
    def __str__(self): return self.content

# ==========================================
# 3. 가상 파일 시스템 (VFS - 폴더 & 파일)
# ==========================================
class Folder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='folders')
    # 💡 자기 참조(self)를 통해 폴더 안에 폴더를 무한히 넣을 수 있게 합니다.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders', verbose_name="상위 폴더")
    name = models.CharField(max_length=100, verbose_name="폴더명")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=100, verbose_name="파일명 (예: main.py)")
    last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="마지막 수정자")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): return self.name


class ProjectBlock(models.Model):
    """Jupyter Notebook의 Cell 역할을 하는 블록 모델"""
    BLOCK_TYPES = (
        ('markdown', 'Markdown'),
        ('code', 'Code'),
        # 이미지 업로드 확장을 대비한 타입
        ('image', 'Image'), 
    )
    
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES, default='markdown')
    content = models.TextField(blank=True, verbose_name="블록 내용")
    order = models.PositiveIntegerField(default=0, verbose_name="배치 순서")
    
    class Meta:
        ordering = ['order']

    
class ProjectMemo(models.Model):
    # 💡 기존 필드: 블록이 아니라 '파일' 자체에 댓글을 달 수 있도록 연결을 파일로 변경하는 것이 좋습니다.
    file = models.ForeignKey('File', on_delete=models.CASCADE, related_name='memos', null=True) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="메모 내용")
    created_at = models.DateTimeField(auto_now_add=True)

    # 💡 새로 추가된 피드백/수정요청 필드
    target_line = models.PositiveIntegerField(null=True, blank=True, verbose_name="지정된 코드 라인")
    is_request = models.BooleanField(default=False, verbose_name="수정 요청 여부")
    is_resolved = models.BooleanField(default=False, verbose_name="해결 여부")


# ==========================================
# 5. 소통 (팀 커뮤니티) 및 알림 시스템
# ==========================================
class ProjectDiscussion(models.Model):
    """프로젝트 전체에 대한 피드백 및 공지용 커뮤니티"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    """로그인한 유저가 우측 상단 메일함에서 볼 수 있는 알림"""
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="수신자")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications', verbose_name="발신자")
    message = models.CharField(max_length=255, verbose_name="알림 내용")
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name="이동할 링크 (선택)")
    is_read = models.BooleanField(default=False, verbose_name="읽음 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']