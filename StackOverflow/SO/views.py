from django.shortcuts import render
from django.core.paginator import Paginator

QUEST_NUMBER = 10
ANSWER_NUMBER = 5

QUESTIONS = [
    {
        "id": f"{i}",
        "title": f"Question {i}", 
        "text": f"This is question {i}"
    } 
    for i in range(60)
]

ANSWER = [
    {
        "title": f"Answer {i+1}", 
        "text": f"Hello everyone"
    } 
    for i in range(3)
]

def pagination(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def newask(request):
    return render(request, 'newask.html')

def ask(request):
    page_obj = pagination(QUESTIONS, request, QUEST_NUMBER)
    return render(request, 'ask.html', {'questions': page_obj, 'is_auth': True})

def setting(request):
    data = {'login': 'ilovepenza', 'email': 'kreed@mail.ru', 'name': 'Egor Kreed'}
    return render(request, 'setting.html', {'user': data})

def hot(request):
    questions = pagination(QUESTIONS[9:], request, QUEST_NUMBER)
    return render(request, 'hot.html', {"questions": questions})

def answer(request, question_id):
    try:
        question_id = int(question_id)
        question = QUESTIONS[question_id]
    except (ValueError, IndexError):
        return render(request, 'ask.html', {"questions": QUESTIONS})
    page_obj = pagination(QUESTIONS, request, QUEST_NUMBER)
    return render(request, 'answer.html', {"question": question, "answers": ANSWER, 'page_obj': page_obj})

def tag(request):
    data = {'title': 'tag'}
    questions = pagination(QUESTIONS, request, QUEST_NUMBER)
    return render(request, 'tag.html', {'tag': data, "questions": questions})

def reg(request):
    return render(request, 'registration.html')

def login(request):
    return render(request, 'login.html')
