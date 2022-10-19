from django.shortcuts import render,redirect

from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
# models
from .models import *

# Create your views here.
def signup(request):
    if request.method=="POST":
        f_name=request.POST.get('first_name')
        l_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password1=request.POST.get('password')
        password2=request.POST.get('con_password')
        if password1!=password2:
            messages.error(request,'Password Not Matched')
            return redirect('register')
        if User.objects.filter(username=username):
            messages.warning(request,"Username Already exists!!")
            return render('register')
        if User.objects.filter(email=email):
            messages.warning(request,'Email already registred')
            return render('register')
        if len(password1)<6:
            messages.warning(request,'Password length not Less than 6')
            return render('register')
        else:
            newuser=User.objects.create_user(username=username,email=email,password=password1,first_name=f_name,last_name=l_name)
            newuser.save()
            messages.success(request,"You Account has been succesfully created")
            return redirect('signin')
    return render(request,'home.html')

def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['password']
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Bad Credential!')
            return redirect('signin')
    return render(request,'home.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request,'You are successfully logout')
    return redirect('signin')

@login_required
def home(request):
    topics=Topic.objects.all()
    p=Paginator(McqQuestion.objects.all().order_by('-id'),15)
    page=request.GET.get('page')
    ques=p.get_page(page)
    context={
        'topics':topics,
        'questions':ques
    }
    return render(request,'homepage.html',context)

@login_required
def selected_topic(request,topic_id):
    p=Paginator(McqQuestion.objects.filter(topic_id=topic_id).order_by('-id'),15)
    page=request.GET.get('page')
    ques=p.get_page(page)
    topics=Topic.objects.all()
    context={
        'topics':topics,
        'questions':ques
    }
    return render(request,'topicMcq.html',context)

# add mcq question
@login_required
def add_mcq_topic(request):
    superusers=User.objects.filter(is_superuser=True)
    current_user=request.user
    isnot_superuser=current_user not in superusers
    if request.method=='POST':
        topic=request.POST.get('topic')
        user_Alltopic=current_user.user_mcq_topic.all()
        if len(user_Alltopic)>2 and isnot_superuser:
            messages.error(request,'Cannot Add More, Already Added 3')
            return redirect('home')
        if Topic.objects.filter(topic=topic):
            messages.error(request,'Topic Already Added')
            return redirect('add_mcq_question')
        else:
            new_topic=Topic.objects.create(user=current_user,topic=topic)
            new_topic.save()
            return redirect('add_mcq_question')

@login_required
def add_mcq_question(request):
    mcq_topics=Topic.objects.all()
    mcq_questions=McqQuestion.objects.all()
    context={
        'mcq_topics':mcq_topics,
        'mcq_questions':mcq_questions
    }
    superusers=User.objects.filter(is_superuser=True)
    curr_user=request.user
    isnot_superuser=curr_user not in superusers
    if request.method=='POST':
        topic=request.POST.get('topic')
        question=request.POST.get('mcqquestion')
        user_Allmcq=curr_user.user_question.all()
        if len(user_Allmcq)>4 and isnot_superuser:
            messages.error(request,'Cannot Add More Question, Already Added 5')
            return redirect('home')
        if McqQuestion.objects.filter(question=question):
            messages.error(request,'Question Already Added')
            return redirect('home')
        else:
            topic_id=Topic.objects.filter(topic=topic)[0]
            new_mcq_que=McqQuestion.objects.create(user=curr_user,topic_id=topic_id.id,question=question)
            new_mcq_que.save()
            return redirect('add_mcq_question')
    return render(request,'add_mcq_question.html',context)

@login_required
def add_mcq_option(request):
    if request.method=='POST':
        question=request.POST.get('question')
        option=request.POST.get('mcqqueOption')      
        ques_id=McqQuestion.objects.filter(question=question)[0]        
        allquestionOption=QuestionOption.objects.filter(id=ques_id.id)
        if QuestionOption.objects.filter(mcq_question_id=ques_id.id,option=option):
            messages.error(request,'This option Already Added for this Question')
            return redirect('add_mcq_question')
        if len(allquestionOption)>6:
            messages.error(request,'Cannot Add More, Already Added 7')
            return redirect('add_mcq_question')
        new_option=QuestionOption.objects.create(mcq_question_id=ques_id.id,option=option)
        is_correctopt=request.POST.get('iscrrt')  
        if is_correctopt:
            new_option.is_correct=is_correctopt
        new_option.save()
        return redirect('add_mcq_question')
    
@login_required
def search(request):
    searched_data=""
    if request.method=='POST':
        searched_data=request.POST.get('searched_data')
    mcq_topics=Topic.objects.filter(topic__contains=searched_data).order_by('id')
    p=Paginator(McqQuestion.objects.filter(question__contains=searched_data).order_by('-id'),15)
    page=request.GET.get('page')
    ques=p.get_page(page)
    context={
        'keyword':searched_data,
        'mcq_topics':mcq_topics,
        'questions':ques,
    }
    return render(request,'search.html',context)

@login_required
def contactus(request):
    curr_user=request.user
    if request.method=='POST':
        message=request.POST.get('message')
        new_message=Message(user=curr_user,message=message)
        new_message.save()
        messages.info(request,'Message Send')
        return redirect('home')
    return render(request,'contactUs.html')
