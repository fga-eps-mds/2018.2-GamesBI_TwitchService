import requests

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stream, User, Game
from .serializers import StreamSerializer


class TwitchView(APIView):

    '''
            View that calls Twitch API
            and return some relevant
            information about a stream
            and filter for Null value
    '''
    def get(self, request, format=None):

        games_name = ['The walking dead', 'fortnite']

        for game_name in games_name:
            game_data = self.get_game_data(game_name)
            filtered_game_data = self.filter_game_data(game_data)
            stream_data = self.get_stream_data(filtered_game_data['id'])
            filtered_stream_data = self.filter_stream_data(stream_data)
            user_data = self.get_user_data(filtered_stream_data['user_id'])
            filtered_user_data = self.filter_user_data(user_data)
            self.save_stream(filtered_game_data, filter_stream_data)
            self.save_user(filtered_user_data)

        streams = Stream.objects.all()
        for stream in streams:
            print('------------')
            print(stream.id)
            print(stream.game_id)
            print(stream.game_name)
            print(stream.language)
            print(stream.started_at)
            print(stream.type)
            print(stream.viewer_count)

            users = User.objects.all()
            for user in users:
                print(user.id)
                print(user.display_name)
                print(user.type)
                print(user.view_count)
                print(user.follows)

            print('------------')

        return Response(data=games_name)

    def get_game_data(self, game_name):
        game_name = []

        for game_name in games_name:
            url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            gamedata = requests.get(url, headers=header)
            ndata = gamedata.json() #retorna game_name, game_id

        return ndata

    def filter_game_data(self, game_data):

        if 'id' in game_data:
            id = game_data['id']
        else:
            id = None

        if 'name' in game_data:
            name = game_data['name']
        else:
            name = None

        filtered_game_data = {
        'id': id,
        'name': name,
        }

        return filtered_game_data

    def get_stream_data(self, game_id_list):
        game_id = []

        for game_id in game_id_list:
            url = 
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            streamdata = requests.get(url, headers=header)
            ndata = streamdata.json() 

        return ndata

    def filter_stream_data(self, stream_data):

        if 'id' in stream_data:
            id = stream_data['id']
        else:
            id = None


    def get_user_data(self, user_id_list):
        user_id = []

        for user_id in user_id_list:
            url = 
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            userdata = request.get(url, headers=header)
            ndata = userdata.json()

        return ndata

    def filter_user_data(self, user_data):



    def save_stream(self, game_list, stream_list):
        stream = Stream(
        id = stream_list['id'],
        game_id = game_list['id'],
        game_name = game_list['name'],
        language = stream_list['language'],
        started_at = stream_list['started_at'],
        type = stream_list['type'],
        viewer_count = stream_list['viewer_count']
        )

        stream.save()

        print('a stream do jogo {} foi salva '.format(stream.game_name)) 

    def save_user(self, user_list):
        user = User(
        id = user_list['user_id'],
        display_name = user_list['display_name'],
        type = user_list['type'],
        view_count = user_list['view_count'],
        follows = user_list['follows']
        )

        user.save()

        print('o user {} foi salvo'.format(user.id)) 
