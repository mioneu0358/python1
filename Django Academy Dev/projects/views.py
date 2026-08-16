from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyJournal
import json
import uuid
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from .models import *
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def api_search_users(request):
    """참여 인원 검색용 API (이름으로 검색, 수퍼유저 제외)"""
    query = request.GET.get('q', '').strip()
    users_data = []
    
    if query:
        # 슈퍼유저 제외, 이름이 포함된 유저 검색
        matched_users = User.objects.filter(is_superuser=False).filter(
            Q(name__icontains=query) | Q(username__icontains=query)
        )[:10] # 최대 10명 제한
        
        for u in matched_users:
            email_prefix = u.email.split('@')[0] if u.email else 'no-email'
            users_data.append({
                'id': u.id,
                'name': getattr(u, 'name', u.username),
                'email_prefix': email_prefix
            })
            
    return JsonResponse({'users': users_data})

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


@login_required
def project_list(request):
    # 1. 파라미터 가져오기
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'title')
    sort = request.GET.get('sort', '-updated_at') # 기본값: 최신순
    
    # 2. 기본 쿼리셋 (전체 프로젝트)
    projects = Project.objects.all()
    
    # 3. 검색 처리
    if query:
        if search_type == 'title':
            projects = projects.filter(title__icontains=query)
        elif search_type == 'participants':
            projects = projects.filter(participants__name__icontains=query)
        elif search_type == 'class':
            projects = projects.filter(study_class__name__icontains=query)
            
    # 4. 정렬 처리 (수정일 기준)
    if sort == 'updated_at':
        projects = projects.order_by('updated_at') # 과거순
    else:
        projects = projects.order_by('-updated_at') # 최신순 (내림차순)
        
    # 5. 페이징 처리 (한 페이지당 10개씩)
    paginator = Paginator(projects.distinct(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 다음 렌더링 시 현재 검색/정렬 상태를 유지하기 위해 컨텍스트에 담아 보냄
    context = {
        'page_obj': page_obj,
        'query': query,
        'search_type': search_type,
        'sort': sort,
    }
    return render(request, 'project_list.html', context)

@login_required
def project_create(request):
    """프로젝트 생성 및 동적 블록 저장 뷰"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            class_id = data.get('class_id')
            blocks = data.get('blocks', []) # 프론트에서 넘어온 블록 배열

            # 1. 프로젝트 뼈대 생성
            project = Project.objects.create(
                title=title,
                study_class_id=class_id if class_id else None
            )
            # 프로젝트 생성자를 참여 인원으로 기본 추가
            project.participants.add(request.user)

            # 2. 전달받은 블록(Cell)들을 순서대로 저장
            for index, block in enumerate(blocks):
                ProjectBlock.objects.create(
                    project=project,
                    block_type=block.get('type'),
                    content=block.get('content'),
                    order=index
                )
            
            # 저장 성공 시 게시판 목록으로 리다이렉트 URL 반환
            return JsonResponse({'status': 'success', 'redirect_url': '/projects/list/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)

    # GET 요청 시 화면 렌더링 (참여 가능한 반 목록 전달)
    classes = StudyClass.objects.all()
    return render(request, 'project_create.html', {'classes': classes})

@login_required
def upload_image(request):
    """마크다운 에디터에서 드래그 앤 드롭한 이미지를 저장하고 URL을 반환"""
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']
        
        # 파일명 중복을 막기 위해 랜덤한 UUID로 이름 변경
        ext = img.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        
        fs = FileSystemStorage()
        # media/markdown_images/ 폴더 안에 저장됨
        saved_name = fs.save(f"markdown_images/{filename}", img)
        image_url = fs.url(saved_name)
        
        return JsonResponse({'url': image_url})
        
    return JsonResponse({'error': '업로드 실패'}, status=400)

@login_required
def project_detail(request, pk):
    """프로젝트 상세 보기 화면 (블록 및 메모 렌더링)"""
    project = get_object_or_404(Project, pk=pk)
    # prefetch_related로 메모 작성자 정보까지 한 번에 최적화해서 불러옵니다.
    blocks = project.blocks.all().prefetch_related('memos', 'memos__author')
    
    return render(request, 'project_detail.html', {
        'project': project,
        'blocks': blocks,
    })

@login_required
def add_memo(request, block_id):
    """특정 블록에 메모(댓글)를 추가하는 비동기 API"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        content = data.get('content', '').strip()
        
        if content:
            block = get_object_or_404(ProjectBlock, pk=block_id)
            memo = ProjectMemo.objects.create(
                block=block,
                author=request.user,
                content=content
            )
            return JsonResponse({
                'status': 'success',
                'author_name': memo.author.name if hasattr(memo.author, 'name') else memo.author.username,
                'content': memo.content,
                'created_at': memo.created_at.strftime('%m/%d %H:%M')
            })
    return JsonResponse({'status': 'error', 'msg': '메모 내용을 입력해주세요.'}, status=400)

@login_required
def project_edit(request, pk):
    """기존 프로젝트 수정 뷰"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            # 1. 기본 정보 업데이트
            project.title = data.get('title')
            class_id = data.get('class_id')
            project.study_class_id = class_id if class_id else None
            project.save()

            # 2. 기존 블록 삭제 및 새 블록으로 덮어쓰기 (가장 깔끔한 동적 데이터 업데이트 방식)
            project.blocks.all().delete()
            
            blocks = data.get('blocks', [])
            for index, block in enumerate(blocks):
                ProjectBlock.objects.create(
                    project=project,
                    block_type=block.get('type'),
                    content=block.get('content'),
                    order=index
                )
            
            # 저장 성공 시 상세 페이지로 다시 이동
            return JsonResponse({'status': 'success', 'redirect_url': f'/projects/{project.pk}/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)

    # GET 요청 시 화면 렌더링 (기존 데이터 세팅)
    classes = StudyClass.objects.all()
    
    # 파이썬의 블록 객체들을 자바스크립트가 읽을 수 있도록 리스트/사전 형태로 변환
    blocks_data = []
    for block in project.blocks.all():
        blocks_data.append({
            'type': block.block_type,
            'content': block.content
        })
    import json
    blocks_json = json.dumps(blocks_data)

    return render(request, 'project_edit.html', {
        'project': project,
        'classes': classes,
        'blocks_json': blocks_json
    })