from django.conf.urls import url
from django.contrib import admin
from my_app.views import index, registration
from my_app.views import post

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url( r'^post/([0-9]+)/$', post, name = 'post'),
    url( r'^registration/', registration, name = 'registration'),
    url( r'', index, name = 'index')

]
