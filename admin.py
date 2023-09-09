from django.contrib import admin

# Register your models here.
from .models import Nest, Topic, Message, JoinRequest

admin.site.register(Nest)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(JoinRequest)