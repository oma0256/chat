from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    user_1 = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_1')
    user_2 = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_2')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.id)


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
