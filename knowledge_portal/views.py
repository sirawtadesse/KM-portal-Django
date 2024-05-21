from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import UploadedFile
from .forms import UploadFileForm
from .forms import MyModelForm
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MessageUser, Contact
from .forms import MessageForm
from .models import Question, Response, CodeSnippet
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
from .models import BlogPost, Room, Message,FAQ, Tag, Post
from .forms import BlogPostForm, PostForm
from django.views.generic import TemplateView
from django.db.models import Q


# Create your views here.

def home(request):
    return render(request,'knowledge_portal/home.html')


def about (request):
    return render(request,'knowledge_portal/about.html')


class SearchView(TemplateView):
    template_name = "knowledge_portal/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = Post.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw))
        code_results = CodeSnippet.objects.filter(Q(title__icontains=kw))
        asks = FAQ.objects.filter(Q(question__icontains=kw))
        rom = Room.objects.filter(Q(name__icontains=kw))
        blogs = BlogPost.objects.filter(Q(title__icontains=kw) | Q(content__icontains=kw) | Q(image__icontains=kw))
        ques = Question.objects.filter(Q(title__icontains=kw) | Q(body__icontains=kw))
        msgs = MessageUser.objects.filter(Q(subject__icontains=kw) | Q(body__icontains=kw))
        print(results)
        print(code_results)
        print(asks)
        print(rom)
        print(blogs)
        print(ques)
        print(msgs)
        context['results'] = results
        context['code_results'] = code_results
        context['asks'] = asks
        context['rom'] = rom
        context['blogs'] = blogs
        context['ques'] = ques
        context['msgs'] = msgs
        return context


def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'knowledge_portal/faq_list.html', {'faqs': faqs})

@login_required(login_url='login')
def create_post(request):
    posts = BlogPost.objects.all()  # Retrieve all posts
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('create_post')  # Redirect to the same page after creating the post
    else:
        form = BlogPostForm()
    return render(request, 'knowledge_portal/create_post.html', {'form': form, 'posts': posts})

@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'knowledge_portal/edit_post.html', {'form': form, 'post': post})


@login_required(login_url='login')
def communications(request):
    return render(request, 'knowledge_portal/communications.html')


def room(request, room):
    username = request.GET.get('username') # henry
    room_details = Room.objects.get(name=room)
    return render(request, 'knowledge_portal/room.html', {

        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    # return HttpResponse("Hi, Message Sent Successfully!!")

def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})

@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_file')
    else:
        form = UploadFileForm()
    files = UploadedFile.objects.all()
    return render(request, 'knowledge_portal/upload_file.html', {'form': form, 'files': files})

def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response

def editor(request):
    form = MyModelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        content = form.cleaned_data['content']  # Assuming 'content' is the name of your text field

        # Create an HTTP response with the file content as an attachment
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="file.txt"'
        
        return response

    return render(request, 'knowledge_portal/editor.html', {'form': form})



def snippet_list(request):
    snippets = CodeSnippet.objects.all()
    return render(request, 'knowledge_portal/snippet_list.html', {'snippets': snippets})


@login_required
def email(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('email')  # Redirect to the same page after sending the message
    else:
        form = MessageForm()

    received_messages = MessageUser.objects.filter(recipient=request.user).order_by('-timestamp')

    return render(request, 'knowledge_portal/email.html', {
        'form': form,
        'received_messages': received_messages
    })


@login_required
def read_message(request, message_id):
    message = get_object_or_404(MessageUser, id=message_id)
    return render(request, 'knowledge_portal/read_message.html', {'message': message})


def contact(request):
    if request.method == 'POST':
        cont = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        cont.name=name
        cont.email=email
        cont.subject=subject
        cont.save()
        return HttpResponse("<h1>Thanks For Contact Us</h1>")
    return render(request, 'knowledge_portal/contact.html')


def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('homepage')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'knowledge_portal/register.html', context)

def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('homepage')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'knowledge_portal/login.html', context)

@login_required(login_url='register')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='register')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'knowledge_portal/new-question.html', context)

def homePage(request):
    questions = Question.objects.all().order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'knowledge_portal/homepage.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'knowledge_portal/question.html', context)


@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('homepage')

       

def article_list(request):
    posts = Post.objects.all()
    return render(request, 'knowledge_portal/article_list.html', {'posts': posts})

@login_required
def create_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('article_list')
    else:
        form = PostForm()
    return render(request, 'knowledge_portal/create_article.html', {'form': form})
