from django.db import models
from django.db.models import Manager, Count
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProfileManager(models.Manager):
    def profile_top(self):
        return self.order_by('-rating') [:5] 

class Profile(models.Model):
    profile_id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    avatar = models.ImageField(upload_to='static/img/avatar', blank=True, null=True, default='static/img/default.jpg')
    rating=models.IntegerField(default=0)
    manager=ProfileManager()

    def __str__(self):
        return f'{self.profile_id}, {self.user}'


class TagManager(models.Manager):
    def tag_top(self):
        return self.annotate(count=Count('questions')).order_by('-count') [:5]
    def tag_question(self, question):
        return self.filter(questions=question)

class Tag(models.Model):
    tag_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    manager=TagManager()

    def __str__(self):
        return f'{self.tag_id}, {self.name}'

class QuestionManager(models.Manager):
    def question_top(self):
        return self.order_by('-grade')
    def question_date(self):
        return self.order_by('-created_at') 
    def question_with_tag(self, tag):
        return self.filter(tags=tag).order_by('-grade')

class Question(models.Model):
    question_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    text=models.CharField(max_length=2000)
    tags=models.ManyToManyField(Tag, blank=True, related_name='questions')
    grade = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    manager=QuestionManager()
    que_user=models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='que_user')

    def __str__(self):
        return f'{self.question_id}, {self.que_user}: {self.title}'
    
    def clean(self):
        if self.tags.count() > 3:
            raise ValidationError('A question cannot have more than 3 tags.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def add_tag(self, tag):
        if self.tags.count() >= 3:
            raise ValidationError('A question cannot have more than 3 tags.')
        self.tags.add(tag)

class AnswerManager(models.Manager):
    def answer_date(self,question):
        return self.filter(ans_question=question).order_by('-created_at') 

class Answer(models.Model):
    answer_id=models.AutoField(primary_key=True)
    ans_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    author=models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='answers')
    ans_title=models.CharField(max_length=100)
    ans_text=models.CharField(max_length=2000)
    ans_grade=models.IntegerField(default=0)
    is_correct=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    manager=AnswerManager()

    def __str__(self):
        return f'{self.answer_id}, {self.author}: {self.ans_question}'

class ReactionToQuestion(models.Model):
    user_like = models.ForeignKey('Profile', on_delete=models.PROTECT, related_name='user_like')
    question_like = models.ForeignKey('Question', on_delete=models.PROTECT, related_name='question_like')
    answer_like = models.ForeignKey('Answer', on_delete=models.PROTECT, related_name='answer_like')
    CHOICE = [
        ("Like", "like"),
        ("Dislike", "dislike"),
    ]
    class Meta:
        unique_together=[('user_like','question_like'), ('user_like', 'answer_like')]
    like=models.CharField(max_length=7, choices=CHOICE)    

    def __str__(self):
        return f'{self.id}, {self.CHOICE}: {self.user_like} estimate {self.question_like}'
    