from django.contrib import admin
from .models import  CodeSnippet,FAQ,Post, Tag, Message, Room, BlogPost, Response, Question, MessageUser, Contact, MyModel, UploadedFile

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(UploadedFile)
admin.site.register(Message)
admin.site.register(MessageUser)
admin.site.register(BlogPost)
admin.site.register(Room)
admin.site.register(Response)
admin.site.register(Question)
admin.site.register(Contact)
admin.site.register(MyModel)
admin.site.register(CodeSnippet)
admin.site.register(FAQ)