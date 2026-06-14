from django.shortcuts import render

def index(request):
    dummy_projects = [
        {"title": "프로젝트 1", "description": "첫 번째 프로젝트에 대한 간단한 설명입니다."},
        {"title": "프로젝트 2", "description": "두 번째 프로젝트에 대한 간단한 설명입니다."},
        {"title": "프로젝트 3", "description": "세 번째 프로젝트에 대한 간단한 설명입니다."},
    ]
    
    context = {
        'owner_name': '찬빈', # 사이트 주인 이름
        'projects': dummy_projects
    }
    return render(request, 'index.html', context)