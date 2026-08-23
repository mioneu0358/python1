from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DailyJournal
import json, os
import uuid
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from .models import *
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def api_search_users(request):
    query = request.GET.get('q', '').strip()
    print(f"search_user_api - query: {query}")
    users_data = []
    
    if query:
        # 슈퍼유저 제외, 이름이 포함된 유저 검색
        matched_users = User.objects.filter(is_superuser=False, name__contains=query)[:10] # 최대 10명 제한
        
        for u in matched_users:
            email_prefix = u.email.split('@')[0] if u.email else 'no-email'
            users_data.append({
                'id': u.id,
                'name': getattr(u, 'name', u.name),
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
    """프로젝트 생성 뷰"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 변경점: classId 대신 teamId를 받습니다.
            team_id = data.get('teamId') 
            
            project = Project.objects.create(
                title=data.get('title'),
                description=data.get('description', ''),
                start_date=data.get('start_date') or None,
                end_date=data.get('end_date') or None,
                team_id=team_id if team_id else None,
                leader_id=data.get('leaderId') or request.user.id
            )

            # 참여 인원 처리
            user_set = set(data.get('participantIds', []))
            user_set.add(str(request.user.id))
            participants = User.objects.filter(id__in=user_set)
            project.participants.set(participants)
            
            if not project.leader or not project.participants.filter(id=project.leader.id).exists():
                project.leader = request.user
                project.save()

            # 단계 및 체크리스트 처리 (기존과 동일)
            for stage_info in data.get('stages', []):
                stage = ProjectStage.objects.create(
                    project=project, 
                    name=stage_info.get('name'), 
                    order=stage_info.get('order', 0),
                    # 💡 새로 추가된 날짜 데이터 받기 (비어있으면 None 처리)
                    start_date=stage_info.get('start_date') or None,
                    end_date=stage_info.get('end_date') or None
                )
                for cl_text in stage_info.get('checklists', []):
                    Checklist.objects.create(stage=stage, content=cl_text)

            return JsonResponse({'status': 'success', 'redirect_url': '/projects/list/'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)

    # GET 요청 시: 내가 속한 팀/그룹 목록을 가져옵니다.
    my_teams = request.user.my_teams.all()
    current_user_name = getattr(request.user, 'name', None) or request.user.username
    
    return render(request, 'project_create.html', {
        'my_teams': my_teams,
        'current_user_name': current_user_name,
    })


@login_required
def api_create_team(request):
    """새로운 팀을 생성하는 비동기 API"""
    if request.method == 'POST':
        data = json.loads(request.body)
        team_name = data.get('name', '').strip()
        member_ids = data.get('member_ids', [])
        
        if team_name and member_ids:
            team = Team.objects.create(name=team_name, creator=request.user)
            # 본인과 선택된 멤버들을 팀에 추가
            team.members.add(request.user)
            team.members.add(*member_ids)
            
            return JsonResponse({
                'status': 'success', 
                'team_id': team.id, 
                'team_name': team.name
            })
    return JsonResponse({'status': 'error', 'msg': '잘못된 요청입니다.'}, status=400)

@login_required
def api_get_team_members(request, team_id):
    """특정 팀의 멤버 목록을 반환하는 API"""
    print("api_get_team_members()호출")
    team = get_object_or_404(Team, pk=team_id)
    members_data = []
    
    for u in team.members.all():
        members_data.append({
            'id': u.id,
            'name': getattr(u, 'name', None) or u.username,
            'email_prefix': u.email.split('@')[0] if u.email else 'no-email'
        })
        
    return JsonResponse({'status': 'success', 'members': members_data})

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


# projects/views.py의 project_detail 함수 수정
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    stages = project.stages.all().prefetch_related('checklists')
    
    # 💡 [추가된 로직] 현재 진행 중인 단계 계산
    # 체크리스트가 하나라도 미완료 상태인 첫 번째 단계를 '현재 단계'로 지정합니다.
    current_stage = None
    for stage in stages:
        total_cl = stage.checklists.count()
        completed_cl = stage.checklists.filter(is_completed=True).count()
        
        # 체크리스트가 아예 없거나, 100% 완료되지 않은 경우 이 단계가 현재 단계임
        if total_cl == 0 or completed_cl < total_cl:
            current_stage = stage
            break
            
    # 모든 단계가 100% 완료되었다면 마지막 단계를 현재 단계로 표시
    if not current_stage and stages.exists():
        current_stage = stages.last()

    root_folders = project.folders.filter(parent__isnull=True)
    
    context = {
        'project': project,
        'stages': stages,
        'current_stage': current_stage, # 템플릿으로 전달
        'root_folders': root_folders,
    }
    return render(request, 'project_detail.html', context)

@login_required
def toggle_checklist(request, pk):
    """체크리스트 완료 상태를 변경하는 비동기 API"""
    if request.method == 'POST':
        checklist = get_object_or_404(Checklist, pk=pk)
        
        # 권한 체크: 프로젝트 참여자나 리더만 체크할 수 있도록 방어 로직 추가 가능
        
        data = json.loads(request.body)
        is_completed = data.get('is_completed', False)
        
        checklist.is_completed = is_completed
        checklist.save()
        
        return JsonResponse({'status': 'success', 'is_completed': checklist.is_completed})
    return JsonResponse({'status': 'error'}, status=400)

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
@login_required
def api_get_vfs_tree(request, project_id):
    """프로젝트의 전체 폴더/파일 구조를 JSON으로 반환"""
    project = get_object_or_404(Project, pk=project_id)
    
    # 최상위(Root) 폴더들만 가져옵니다.
    root_folders = project.folders.filter(parent__isnull=True).prefetch_related('files', 'subfolders')
    
    def build_tree(folders):
        tree = []
        for f in folders:
            tree.append({
                'type': 'folder',
                'id': f.id,
                'name': f.name,
                'files': [{'id': file.id, 'name': file.name} for file in f.files.all()],
                'subfolders': build_tree(f.subfolders.all()) # 재귀적으로 하위 폴더 탐색
            })
        return tree

    return JsonResponse({'status': 'success', 'tree': build_tree(root_folders)})

@login_required
def api_create_folder(request, project_id):
    """새로운 폴더 생성"""
    if request.method == 'POST':
        data = json.loads(request.body)
        project = get_object_or_404(Project, pk=project_id)
        parent_id = data.get('parent_id')
        
        folder = Folder.objects.create(
            project=project,
            name=data.get('name', '새 폴더'),
            parent_id=parent_id if parent_id else None
        )
        return JsonResponse({'status': 'success', 'folder_id': folder.id, 'name': folder.name})

@login_required
def api_create_file(request, project_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        folder = get_object_or_404(Folder, pk=data.get('folder_id'), project_id=project_id)
        
        raw_name = data.get('name', '새 파일').strip()
        name, ext = os.path.splitext(raw_name)
        
        # 💡 확장자가 없으면 기본값으로 .txt 부여
        if not ext:
            ext = '.txt'
        final_name = name + ext
        
        file = File.objects.create(
            folder=folder,
            name=final_name,
            last_modified_by=request.user
        )
        return JsonResponse({'status': 'success', 'file_id': file.id, 'name': file.name})

@login_required
def api_delete_vfs_item(request, project_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_type = data.get('type') # 'folder' or 'file'
        item_id = data.get('id')
        
        project = get_object_or_404(Project, pk=project_id)
        
        # 💡 권한 체크: 팀장이나 참여 인원만 삭제 가능
        if request.user != project.leader and request.user not in project.participants.all():
            return JsonResponse({'status': 'error', 'msg': '삭제 권한이 없습니다.'}, status=403)

        if item_type == 'folder':
            get_object_or_404(Folder, pk=item_id, project=project).delete()
        elif item_type == 'file':
            get_object_or_404(File, pk=item_id, folder__project=project).delete()
            
        return JsonResponse({'status': 'success'})

@login_required
def api_backup_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    # 메모리에 ZIP 파일을 생성 (서버 용량 낭비 방지)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # 재귀적으로 폴더와 파일을 순회하며 ZIP에 담는 내부 함수
        def add_folder_to_zip(folder, current_path=""):
            folder_path = f"{current_path}{folder.name}/"
            # 빈 폴더도 압축 파일에 생성
            zip_file.writestr(folder_path, "")
            
            # 폴더 안의 파일들 추가
            for f in folder.files.all():
                # 파일 내부에 저장된 블록(Code, Markdown)들의 내용을 하나로 합침
                content = "\n\n".join([block.content for block in f.blocks.all()])
                zip_file.writestr(f"{folder_path}{f.name}", content)
                
            # 하위 폴더 탐색
            for sub in folder.subfolders.all():
                add_folder_to_zip(sub, folder_path)
                
        # 최상위 폴더부터 압축 시작
        root_folders = project.folders.filter(parent__isnull=True)
        for root in root_folders:
            add_folder_to_zip(root)
            
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    # 다운로드되는 파일명 설정 (예: 24시간_트레이딩_봇_backup.zip)
    safe_title = project.title.replace(" ", "_")
    response['Content-Disposition'] = f'attachment; filename="{safe_title}_backup.zip"'
    
    return response

@login_required
def project_vfs(request, project_id):
    """파일 탐색기(VFS) 메인 화면 렌더링"""
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project_vfs.html', {'project': project})



@login_required
def api_get_file_content(request, project_id, file_id):
    """파일의 내용(블록)을 가져오는 API"""
    file = get_object_or_404(File, pk=file_id, folder__project_id=project_id)
    blocks = file.blocks.all().order_by('order')
    
    blocks_data = []
    for b in blocks:
        blocks_data.append({
            'id': b.id,
            'type': b.block_type,
            'content': b.content
        })
        
    # 💡 만약 갓 생성된 빈 파일이라 블록이 하나도 없다면, 기본 텍스트 블록을 하나 만들어줍니다.
    if not blocks_data:
        ext = file.name.split('.')[-1].lower()
        default_type = 'code' if ext in ['py', 'cpp', 'html', 'css', 'js'] else 'markdown'
        new_block = ProjectBlock.objects.create(file=file, block_type=default_type, content="", order=0)
        blocks_data.append({'id': new_block.id, 'type': new_block.block_type, 'content': ""})
        
    return JsonResponse({'status': 'success', 'blocks': blocks_data})

@login_required
def api_save_file_content(request, project_id, file_id):
    """파일의 내용을 저장하는 API"""
    if request.method == 'POST':
        file = get_object_or_404(File, pk=file_id, folder__project_id=project_id)
        data = json.loads(request.body)
        
        # 에디터에서 수정한 내용을 받아옵니다
        block_id = data.get('block_id')
        new_content = data.get('content', '')
        
        # 블록 내용 업데이트
        block = get_object_or_404(ProjectBlock, pk=block_id, file=file)
        block.content = new_content
        block.save()
        
        # 파일의 마지막 수정자 업데이트
        file.last_modified_by = request.user
        file.save()
        
        return JsonResponse({'status': 'success'})

def test(request):
    return render(request,'test.html')