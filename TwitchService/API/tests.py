from TwitchService.importdata.models import Stream, Game
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.urls import include, path, reverse
from rest_framework import status
from django.test import TestCase
from model_mommy import mommy
# Create your tests here.
class EndpointTestCase(APITestCase, URLPatternsTestCase):

    urlpatterns= [
        path('api/', include('TwitchService.API.urls'))
    ]

    def setUp(self):

        self.Stream_twitch = mommy.make(
            Game,
            game_id = 0,
            game_name = "aaa",
            total_views = "0",
        )

        self.twitch_endpoint = reverse('request_stream_list')

    def tearDown(self):

        Stream.objects.all().delete()

    def test_status_twitch_endpoint(self):

        response = self.client.get(self.twitch_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_twitch_endpoint(self):

        response = self.client.get(self.twitch_endpoint,format = 'json')

        for data in response.data:
            self.assertNotEqual(data['game_id'], None)
            self.assertNotEqual(data['game_name'], None)
            self.assertNotEqual(data['total_views'], None)
