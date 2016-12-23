from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver


class Answer(models.Model):
    text = models.TextField(verbose_name='answer_text')
    is_correct = models.BooleanField(verbose_name='is_correct', default=False)
    author = models.ForeignKey('Profile', verbose_name='answer_author')
    rating = models.IntegerField(verbose_name='answer_rating', default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('Question', verbose_name='answer_to')

    def __str__(self):
        return self.text


class QuestionManager(models.Manager):
    @staticmethod
    def get_popular():
        return Question.objects.order_by('-rating')

    @staticmethod
    def get_last():
        return Question.objects.order_by('-add_time')

    @staticmethod
    def get_with_tag(tag):
        return Question.objects.filter(tags__name=tag).order_by('-add_time')


class Question(models.Model):
    title = models.CharField(max_length=30, blank=True, verbose_name='question_title')
    text = models.TextField(verbose_name='question_text')
    author = models.ForeignKey('Profile', verbose_name='question_author')
    add_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(verbose_name='question_rating', default=0)
    questions = QuestionManager()
    objects = models.Manager()

    def __str__(self):
        return self.text

    def answers(self):
        return Answer.objects.filter(question=self).order_by('-add_time')
    
    def count_answers(self):
        return Answer.objects.filter(question=self).count()


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='tag')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/', default='avatars/default.jpg')
    registration_data = models.DateField(auto_now_add=True)
    rating = models.IntegerField(verbose_name='rating', default=0)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    value = models.SmallIntegerField(verbose_name='value')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    to_object = GenericForeignKey('content_type', 'object_id')
    from_user = models.ForeignKey('Profile', verbose_name='like_from')

    # def save(self):
    #    self.to_object.rating += self.value
    #    self.to_object.save()
    #    super(Like, self).save()


@receiver(post_save, sender=Like)
def change_rating(**kwargs):
    like_to = kwargs['instance'].to_object
    like_to.rating += kwargs['instance'].value
    like_to.author.rating += kwargs['instance'].value
    like_to.author.save()
    like_to.save()
