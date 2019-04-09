from django.urls import path
from .views import ThreadView, ThreadsView

app_name = 'msg'

urlpatterns = [
    path('', ThreadsView.as_view(), name='threads'),
    path('<username>', ThreadView.as_view(), name='thread'),
]
