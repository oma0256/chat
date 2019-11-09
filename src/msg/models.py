from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.db.models import Q


class ThreadManager(models.Manager):
    def get_thread_or_create(self, sender, reciever):
        print(self.get_queryset())
        threads = self.get_queryset().filter(
            Q(user_1__username=sender, user_2__username=reciever) |
            Q(user_1__username=reciever, user_2__username=sender))
        return threads[0] if threads else \
            Thread.objects.create(user_1=sender, user_2=reciever)


class Thread(models.Model):
    user_1 = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_1_threads')
    user_2 = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_2_threads')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = ThreadManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-updated_at']

    @property
    def latest_message(self):
        messages = self.thread_messages.all()
        return messages[0] if messages else None

    def other_user(self, user):
        return self.user_1.username if user.username == self.user_2.username \
            else self.user_2.username


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,
                               blank=True, related_name='thread_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, related_name='sender_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, related_name='reciever_messages')
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.message)

    class Meta:
        ordering = ['-created_at']


def post_save_message(sender, instance, **kwargs):
    instance.thread.save()


post_save.connect(post_save_message, sender=Message)
