from django.urls import path
from .views import ThreadView

app_name = 'msg'

urlpatterns = [
    path('<username>', ThreadView.as_view(), name='thread'),
]
