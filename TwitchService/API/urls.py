from django.urls import include, path
from .views import GamesTwich

urlpatterns = [
    path('request_stream_list/', GamesTwich.as_view(), name="get_stream"),
]
