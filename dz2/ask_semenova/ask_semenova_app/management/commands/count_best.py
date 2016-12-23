from ask_semenova_app.models import Question
from ask_semenova_app.models import Answer
from ask_semenova_app.models import Tag
from ask_semenova_app.models import Profile
from django.core.management.base import BaseCommand
from django.core.cache import cache
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        difference = datetime.timedelta(days=90)
        tags = Tag.objects.all()
        tags_rating = {}
        for i in tags:
            questions = Question.objects.filter(add_time__gt=datetime.datetime.today() - difference)\
                .filter(tags__name=i.name)
            tags_rating[i] = questions.count()
        best = sorted(tags_rating.items(), key=lambda x: x[1], reverse=True)
        best_tags = []
        for i in best[:10]:
            best_tags.append(i[0])

        cache.delete('best_tags')
        cache.set('best_tags', best_tags)

        difference = datetime.timedelta(days=90)
        profiles = Profile.objects.all()
        users_rating = {}
        for i in profiles:
            questions = Question.objects.filter(add_time__gt=datetime.datetime.today() - difference).filter(author=i)
            answers = Answer.objects.filter(add_time__gt=datetime.datetime.today() - difference).filter(author=i)
            users_rating[i] = questions.count() + answers.count()
        best = sorted(users_rating.items(), key=lambda x: x[1], reverse=True)
        best_users = []
        for i in best[:10]:
            best_users.append(i[0].user.username)
        cache.delete('best_users')
        cache.set('best_users', best_users)
