from django.urls import path
from knowledge_portal import views
from .views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #path('blog/', views.blog, name='blog'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('communications/', views.communications, name='communications'),
    path('article_list/', views.article_list, name='article_list'),
    path('create_article/', views.create_article, name='create_article'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('editor/', views.editor, name='editor'),
    path('email/', views.email, name='email'),
    path('contact/', views.contact, name='contact'),
    path('read/<int:message_id>/', views.read_message, name='read_message'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('homepage/', views.homePage, name='homepage'),
    path('new-question/', views.newQuestionPage, name='new-question'),
    path('question/<int:id>/', views.questionPage, name='question'),
    path('reply/', views.replyPage, name='reply'),  # Corrected: Added trailing slash
    path('snippet_list/', views.snippet_list, name='snippet_list'),
    path('faq_list/', views.faq_list, name='faq_list'),
    path('search/', SearchView.as_view(), name='search'),
    path('<str:room>/', views.room, name="room"),
    path('checkview', views.checkview, name="checkview"),
    path('send', views.send, name="send"),
    path('getMessages/<str:room>/', views.getMessages, name="getMessages"),

]
