import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from TwitchService.importdata.models import Stream, User, Game
from .serializers import StreamSerializer

class GamesTwitch(APIView):
    serializers_class = StreamSerializer
    def get(self, request,format=None):
        serializers = self.serializers_class(Stream.objects.all(),many=True)
        return Response(serializers.data)
