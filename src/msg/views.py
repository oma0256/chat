from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from .forms import MessageForm
from .models import Thread, Message


class ThreadView(LoginRequiredMixin, View):
    form = MessageForm()

    def get_object(self, sender, reciever):
        threads = Thread.objects.filter(Q(user_1=sender, user_2=reciever) |
                                        Q(user_1=reciever, user_2=sender))
        return threads[0] if threads else \
            Thread.objects.create(sender=sender, reciever=reciever)

    def dispatch(self, request, username):
        self.sender = request.user
        self.reciever = get_object_or_404(User, username=username)
        self.thread = self.get_object(self.sender, self.reciever)
        return super().dispatch(request, username)

    def get(self, request, username):
        messages = self.thread.thread_messages.all()
        context = {
            'form': self.form,
            'username': username,
            'messages': messages
        }
        return render(request, 'msg/thread.html', context)

    def post(self, request, username):
        message = request.POST.get('message')
        Message.objects.create(thread=self.thread, sender=self.sender,
                               reciever=self.reciever, message=message)
        return HttpResponseRedirect(reverse('msg:thread',
                                            kwargs={'username': username}))
