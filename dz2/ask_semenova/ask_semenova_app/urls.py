from django.conf.urls import url

from . import views

# urlpatterns = [
#    url(r'^$', views.test, name='test'),
# ]

urlpatterns = [
    url(r'^$', views.LastQuestions.as_view(), name="index"),
    url(r'^hot/$', views.PopularQuestions.as_view(), name="hot"),
    url(r'^tag/(.+)/', views.tag_questions, name="tag"),
    url(r'^question/([0-9]+)/$', views.one_question, name="question"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^signup/$', views.singup, name="signup"),
    url(r'^profile/edit/$', views.settings, name="settings"),
    url(r'^ask/$', views.ask, name="ask"),
    url(r'^like/$', views.like, name="like"),
    url(r'^set_correct/([0-9]+)/$', views.set_correct, name="set_correct"),
    url(r'^search_list/$', views.search_list, name="search_list"),
    url(r'^search/(.+)/$', views.search, name="search"),
]
