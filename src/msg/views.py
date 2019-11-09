from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import MessageForm
from .models import Thread, Message


class ThreadsView(LoginRequiredMixin, View):
    def get(self, request):
        threads = Thread.objects.filter(Q(user_1=request.user) |
                                        Q(user_2=request.user)).distinct()
        context = {
            'threads': threads
        }
        return render(request, 'msg/inbox.html', context)


class ThreadView(LoginRequiredMixin, View):
    form = MessageForm()

    def get_object(self, sender, reciever):
        return Thread.objects.get_thread_or_create(sender.username,
                                                   reciever.username)

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
