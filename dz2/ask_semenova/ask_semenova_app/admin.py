from django.contrib import admin

from .models import Question
from .models import Answer
from .models import Tag
from .models import Like
from .models import Profile


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Profile)
# Register your models here.
