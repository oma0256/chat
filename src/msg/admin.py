from django.contrib import admin
from .models import Message, Thread


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

    class Meta:
        model = Thread

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message)
