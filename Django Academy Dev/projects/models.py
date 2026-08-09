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