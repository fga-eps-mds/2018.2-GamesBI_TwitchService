from django.urls import include, path
from .views import TwitchView

urlpatterns = [
    path('get_stream_list/', TwitchView.as_view(), name="get_stream"),
]
