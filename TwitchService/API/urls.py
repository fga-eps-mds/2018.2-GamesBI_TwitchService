from django.urls import include, path
from .views import GamesTwitch

urlpatterns = [
    path('request_stream_list/', GamesTwitch.as_view(), name="request_stream_list"),
]
