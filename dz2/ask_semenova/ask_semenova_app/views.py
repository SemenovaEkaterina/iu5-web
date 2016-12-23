from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Like, Profile, Answer
from .forms import LoginForm, SignupForm, AskForm, AnswerForm, SettingsForm
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_http_methods
from django.views.generic import View
import requests
from django.core.cache import cache
from django.db.models import Q

# from cgi import parse_qs


def test(request):
    result = []
    result.append("Hello, world!<br><br>\n\n")
    for i in request.GET.keys():
        result.append(str(i) + " = " + str(request.GET[i]) + "<br>\n")
    return HttpResponse(result)


def get_range(page, max_page):
    page = int(page)
    limits = []
    for i in range(-2, 3):
        if (0 < page + i <= max_page):
            limits.append(page + i)
    return limits


def popular_tags():
    # return cache.get('best_tags')
    return ['tag', 'web', 'tag___1', 'tag_2', 'tagdw', 'tag)7']


def popular_users():
    # return cache.get('best_users')
    return ['user', 'qwerty', 'ty', 'web', '123']


class LastQuestions(View):
    def get(self, request):
        questions = Question.questions.get_last().select_related('author')
        questions, max_page = paginate(questions, request)

        current_user = CurrentUser(request.user, questions)
        return render(request, 'questions.html', {'context': questions,
                                                  'type': 'New',
                                                  'popular_tags': popular_tags(),
                                                  'popular_users': popular_users(),
                                                  'range': get_range(questions.number, max_page),
                                                  'user': current_user})


class PopularQuestions(View):
    def get(self, request):
        questions = Question.questions.get_popular().select_related('author')
        questions, max_page = paginate(questions, request)
        current_user = CurrentUser(request.user, questions)
        return render(request, 'questions.html', {'context': questions,
                                                  'type': 'Hot',
                                                  'popular_tags': popular_tags(),
                                                  'popular_users': popular_users(),
                                                  'range': get_range(questions.number, max_page),
                                                  'user': current_user})


def tag_questions(request, tag):
    questions = Question.questions.get_with_tag(tag).select_related('author')
    questions, max_page = paginate(questions, request)
    current_user = CurrentUser(request.user, questions)
    return render(request, 'questions.html', {'context': questions,
                                              'type': 'Tag: ' + tag,
                                              'popular_tags': popular_tags(),
                                              'popular_users': popular_users(),
                                              'range': get_range(questions.number, max_page),
                                              'user': current_user})


def one_question(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answers()
    answers, max_page = paginate(answers, request)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(request.user, question)
            headers = {'Content-Type': 'application/json'}
            requests.post('http://ask-semenova.io/publish/?cid='+str(question_id),
                          json.dumps({'text': answer.text,
                                      'avatar': answer.author.avatar.url,
                                      'rating': answer.rating,
                                      'id': answer.id,
                                      }), headers=headers)
            return HttpResponseRedirect(request.path+'?page='+str(1)+'#'+str(answer.id))
    else:
        form = AnswerForm()
    current_user = CurrentUser(request.user, answers)
    if current_user.name is not None:
        profile = Profile.objects.get(user=request.user)
        if len(Like.objects.filter(from_user=profile, object_id=question.id)) > 0:
            question.disabled = 'disabled'
        else:
            question.disabled = ''
        if request.user == question.author.user:
            is_author = 1
        else:
            is_author = 0
    else:
        is_author = 0

    template = 'question.html'
    page_template = '_question_page.html'

    if request.is_ajax():
        template = page_template
        if float(request.GET.get('page')) > max_page:
            return render(request, template, {})

    return render(request, template, {'form': form,
                                      'question': question,
                                      'answers': answers,
                                      'popular_tags': popular_tags(),
                                      'popular_users': popular_users(),
                                      'range': get_range(answers.number, max_page),
                                      'user': current_user,
                                      'is_author': is_author,
                                      'page_template': page_template,
                                      'max_page': max_page})


def login(request):
    if not request.GET.get('continue') is None:
        redirect_url = '/login/?continue=' + request.GET.get('continue')
    else:
        redirect_url = ''
    if request.method == 'POST':
        if not request.GET.get('continue') is None:
            redirect_url = request.GET.get('continue')
        else:
            redirect_url = '/'
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(str(redirect_url))
            else:
                form.add_error(None, 'invalid login/password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'continue': redirect_url, 'popular_tags': popular_tags()})


@login_required(login_url='/login/', redirect_field_name='continue')
def logout(request):
    if not request.GET.get('continue') is None:
        redirect_url = request.GET.get('continue')
    else:
        redirect_url = '/'
    auth.logout(request)
    return HttpResponseRedirect(str(redirect_url))


def singup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            # user = auth.authenticate(username=profile.user.username,
            #                         password=profile.user.password)
            # auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form,
                                           'popular_tags': popular_tags(),
                                           'type': 'Registration'})


@login_required(login_url='/login/', redirect_field_name='continue')
def settings(request):
    current_user = CurrentUser(request.user, [])
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, user=current_user)
        if form.is_valid():
            # profile = form.save()
            form.save()
            # request.session.cycle_key()
            return HttpResponseRedirect('/')
    else:
        form = SettingsForm({'current_login': current_user.name,
                             'login': current_user.name,
                             'avatar': current_user.avatar,
                             'email': current_user.email},
                             user=current_user)
    return render(request, 'signup.html', {'form': form,
                                           'popular_tags': popular_tags(),
                                           'type': 'Settings',
                                           'user': current_user})


@login_required(login_url='/login/', redirect_field_name='continue')
def ask(request):
    if request.is_ajax():
        form = AskForm({'title': request.POST.get('title'),
                       'text': request.POST.get('text'),
                       'tags': request.POST.get('tags')})
        if form.is_valid():
            question = form.save(request.user)
            return JsonResponse({'question_id': question.id})

    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            return HttpResponseRedirect('/question/' + str(question.id))
    else:
        form = AskForm()
    current_user = CurrentUser(request.user, [])
    return render(request, 'ask.html', {'form': form,
                                        'popular_tags': popular_tags(),
                                        'user': current_user})


@login_required()
@require_http_methods("POST")
def like(request):
    try:
        if request.POST.get('object') == 'question':
            object_to_like = Question.objects.get(id=request.POST.get('id'))
        if request.POST.get('object') == 'answer':
            object_to_like = Answer.objects.get(id=request.POST.get('id'))
        profile = Profile.objects.get(user=request.user)
        value_type = int(request.POST.get('type'))
        Like.objects.create(value=value_type, to_object=object_to_like, from_user=profile)
        response_data = {'rating': object_to_like.rating, 'status': 'ok'}
    except:
        response_data = {'status': 'error'}
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@require_http_methods("POST")
def set_correct(request, answer_id):
    try:
        object_to_correct = Answer.objects.get(id=answer_id)
        object_to_correct.is_correct = not object_to_correct.is_correct
        object_to_correct.save()
        response_data = {'status': 'ok'}
    except:
        response_data = {'status': 'error'}
    return JsonResponse(response_data)


def search_list(request):
    input_text = request.GET.get('text')
    result = []
    for question in Question.objects.filter(Q(text__contains=input_text) | Q(title__contains=input_text)):
        result.append([question.id, question.title, question.text])
    response_data = {'list': result}
    return JsonResponse(response_data)


def search(request, text):
    questions = Question.objects.filter(Q(text__contains=text) | Q(title__contains=text))
    questions, max_page = paginate(questions, request)
    current_user = CurrentUser(request.user, questions)
    return render(request, 'questions.html', {'context': questions,
                                              'type': 'Search',
                                              'popular_tags': popular_tags(),
                                              'popular_users': popular_users(),
                                              'range': get_range(questions.number, max_page),
                                              'user': current_user})


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 4)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return objects, paginator.num_pages


class CurrentUser:
    def __init__(self, user, objects):
        if user.is_authenticated():
            profile = Profile.objects.get(user=user)
            self.name = user.username
            self.avatar = profile.avatar
            self.email = user.email

            for one_object in objects:
                if len(Like.objects.filter(from_user=profile, object_id=one_object.id)) > 0:
                    one_object.disabled = 'disabled'
                else:
                    one_object.disabled = ''
                if type(one_object) == ContentType.objects.get(model='answer').model_class() and one_object.is_correct:
                    one_object.checked = 'checked'
                else:
                    one_object.checked = ''
        else:
            self.name = None
            for one_object in objects:
                one_object.disabled = 'disabled'
