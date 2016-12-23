from ask_semenova_app.models import Question
from ask_semenova_app.models import Answer
from ask_semenova_app.models import Tag
from ask_semenova_app.models import Like
from ask_semenova_app.models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        profiles = []
        questions = []
        for i in range(User.objects.count(), User.objects.count() + 7):
            u = User(username='u_test_user_'+str(i), password='1234')
            u.save()
            p = Profile(user=u, avatar='avatars/'+str(i % 6 + 1)+'.jpg')
            p.save()
            profiles.append(p)

        for i in range(1, 7):
            p = profiles[i - 1]
            q = Question(title='title__'+str(i), text=' text' * i, author=p)
            q.save()
            for j in range(1, i + 1):
                t = Tag.objects.get_or_create(name='tag_' + str(j))
                q.tags.add(t[0])
            q.save()
            for j in range(i, 7):
                p = profiles[j - 1]
                l = Like(value=1, to_object=q, from_user=p)
                l.save()
            questions.append(q)

        for i in range(1, 7):
            for j in range(1, i + 1):
                p = profiles[6 - j]
                q = questions[i - 1]
                a = Answer(text=' answer' * j, author=p, question=q)
                a.save()
                for k in range(1, j):
                    p = profiles[k - 1]
                    l = Like(value=1, to_object=a, from_user=p)
                    l.save()
