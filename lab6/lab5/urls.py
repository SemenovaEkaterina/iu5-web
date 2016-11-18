from django.conf.urls import url
from django.contrib import admin
from my_app.views import index
from my_app.views import post

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url( r'^post/([0-9]+)/$', post, name = 'post'),
    url( r'', index, name = 'index'),

]
