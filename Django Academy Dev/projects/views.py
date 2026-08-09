from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyJournal
import json

@login_required
def std_dashboard_view(request):
    return render(request, 'std_dashboard.html')

@login_required
def get_journals(request):
    """FullCalendar에 렌더링할 일지 데이터를 JSON으로 반환"""
    journals = DailyJournal.objects.filter(student=request.user)
    events = []
    for journal in journals:
        events.append({
            'id': journal.id,
            'title': journal.title,
            'start': journal.date.strftime('%Y-%m-%d'),
            'color': '#4f46e5',
            # 추가된 부분: 상세 내용을 extendedProps 안에 담아서 전송
            'extendedProps': {
                'content': journal.content
            }
        })
    return JsonResponse(events, safe=False)

@login_required
def save_journal(request):
    """모달에서 Fetch API로 보낸 데이터를 DB에 저장"""
    if request.method == 'POST':
        data = json.loads(request.body)
        date_str = data.get('date')
        title = data.get('title')
        content = data.get('content')
        
        # update_or_create: 해당 날짜에 이미 일지가 있으면 업데이트, 없으면 새로 생성
        journal, created = DailyJournal.objects.update_or_create(
            student=request.user,
            date=date_str,
            defaults={
                'title': title, 
                'content': content
            }
        )
        return JsonResponse({'status': 'success', 'msg': '저장되었습니다.'})
    
    return JsonResponse({'status': 'fail'}, status=400)

@login_required
def delete_journal(request):
    """모달에서 삭제 요청 시 해당 날짜의 일지 삭제"""
    if request.method == 'POST':
        data = json.loads(request.body)
        date_str = data.get('date')
        
        # 현재 로그인한 학생의 해당 날짜 일지를 찾아 삭제
        DailyJournal.objects.filter(student=request.user, date=date_str).delete()
        
        return JsonResponse({'status': 'success', 'msg': '삭제되었습니다.'})
    return JsonResponse({'status': 'fail'}, status=400)