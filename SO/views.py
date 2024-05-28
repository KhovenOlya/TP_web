from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from SO.models import Question, Tag, Answer
from django.http import HttpResponse

def newask(request):
    return render(request, 'newask.html')

def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj

def ask(request):
    questions=Question.manager.question_date()
    if questions == None:
        return HttpResponse(f"Такой страницы не существует")
    tags_top=Tag.manager.tag_top()
    page_obj = paginate(questions, request)
    return render(request, 'ask.html', {'data': {'title': 'Questions','text': page_obj, 'tag_top': tags_top,},'is_auth': True})


def setting(request):
    data={'login': 'ilovePenza', 'email': 'kreed@mail.ru', 'name': 'Egor Kreed'}
    return render( request, 'setting.html', {'user': data})
     
def hot(request):
    questions=Question.manager.question_top()
    if questions == None:
        return HttpResponse(f"Такой страницы не существует")
    page_obj = paginate(questions, request)
    return render(request, 'hot.html', {'data': {'title': 'Hot questions','text': page_obj}} )
    

def answer(request, question_id):
    question = Question.manager.filter(question_id=question_id).first()
    answers = Answer.manager.filter(ans_question=question)
    page_obj = paginate(answers, request)
    if question is None:
        return HttpResponse("Нет такого вопроса")  
    if not answers.exists():
        return HttpResponse("Нет ответов для этого вопроса")
    return render(request, 'answer.html', {'data': {'title': question.title, 'question': question, 'answers': page_obj, 'grade': question.grade}})



def tag(request, tag_id):
    tag=Tag.manager.get(tag_id = tag_id)
    questions=Question.manager.question_with_tag(tag)
    if questions == None:
        return HttpResponse(f"Такого тега не существует")
    elif questions.count==0:
        return HttpResponse(f"Нет вопросов для этого тега")
    for question in questions:
        if question.tags.count() > 3:
            questions = questions.exclude(pk=question.pk)
    tags_top=Tag.manager.tag_top()
    page_obj = paginate(questions, request)
    print("Questions:", questions)
    return render( request, 'tag.html', {'data':{'title': 'Tag {}'.format(tag_id), 'tags_top': tags_top, 'text': page_obj}})

def reg(request):
    return render(request, 'registration.html')

def login(request): 
    return render(request, 'login.html')

 

