from email import message
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_mcq_topic',null=True)
    topic=models.CharField(max_length=100)

    def __str__(self):
        return self.topic

class McqQuestion(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_question')
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='topic_question')
    question=models.TextField()

    def __str__(self):
        return self.question

class QuestionOption(models.Model):
    mcq_question=models.ForeignKey(McqQuestion,on_delete=models.CASCADE,related_name='question_option')
    option=models.TextField()
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.option

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_message')
    message=models.TextField()

    def __str__(self):
        return self.message
