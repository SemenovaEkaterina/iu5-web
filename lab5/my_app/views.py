from django.shortcuts import render

def index(request):
    posts = []
    for i in range(10):
        posts.append({ 'header':'header ' + str(i), 'text': ( ' text ' + str(i) ) * 20, 'id': i })
    return render(request, "index.html", { 'posts': posts })

def post(request, id):
    return render(request, "post.html", { 'post': {'header': id, 'text': ( ' text ' + str(id) ) * 40, 'id': id, 'rate': int(id) * 10} })