from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='signin'),
    path('signup/',views.signup,name='register'),    
    path('signout/',views.signout,name='signout'),
    path('home/',views.home,name='home'),    
    path('MCQ-Topic/<topic_id>',views.selected_topic,name='topicmcq'),
    # add mcq question
    path('addMcqQuestion/',views.add_mcq_question,name='add_mcq_question'),
    path('addMcqTopic/',views.add_mcq_topic,name='add_mcq_topic'),
    path('addMcqQuestionOption/',views.add_mcq_option,name='add_mcq_option'),
    # search api
    path('seaching/',views.search,name='searching'),
    # contact us api
    path('Contact-Us/',views.contactus,name='ContactUs'),
]