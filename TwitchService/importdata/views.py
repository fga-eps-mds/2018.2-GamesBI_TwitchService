import requests
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Stream, User
from .serializers import StreamSerializer


class TwitchView(APIView):

    '''
            View that calls Twitch API
            and return some relevant
            information about a stream
            and filter for Null value
    '''
    def get(self, request, format=None):

        Stream.objects.all().delete()
        User.objects.all().delete()

        games_name = ['fortnite']
        '''
        url = 'http://localhost:8000/get_igdb_games_list/Name'
        header = {'Accept': 'application/json'}

        names_data = requests.get(url, headers=header)
        games_name = names_data.json()
        '''

        for game_name in games_name:
            game_data = self.get_game_data(game_name)
            filtered_game_data = self.filter_game_data(game_data)
            stream_data = self.get_stream_data(filtered_game_data['id'])
            filtered_stream_data = self.filter_stream_data(stream_data)
            user_data = self.get_user_data(filtered_stream_data['user_id'])
            filtered_user_data = self.filter_user_data(user_data)
            self.save_stream(filtered_game_data, filtered_stream_data)
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
            print(stream.user_id)

            users = User.objects.all()
            for user in users:
                print(user.id)
                print(user.display_name)
                print(user.type)
                print(user.view_count)
                print(user.follows)

            print('------------')

        return Response(data=games_name)

    def get_game_data(self, games_name):
        game_name = []

        for game_name in games_name:
            url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            gamedata = requests.get(url, headers=header)
            ndata = gamedata.json()

        return ndata

    def filter_game_data(self, game_data):

        if 'id' in game_data:
            id = game_data['id']
        else:
            id = '33214'

        if 'name' in game_data:
            name = game_data['name']
        else:
            name = None

        filtered_game_data = {
        'id': id,
        'name': name
        }

        return filtered_game_data

    def get_stream_data(self, game_id_list):
        game_id = []

        for game_id in game_id_list:
            url =  'https://api.twitch.tv/helix/streams?id={}'.format(game_id)
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            streamdata = requests.get(url, headers=header)
            ndata = streamdata.json() 

        return ndata

    def filter_stream_data(self, stream_data):

        if 'id' in stream_data:
            id = stream_data['id']
        else:
            id = '30328259280'

        if 'game_id' in stream_data:
            game_id = stream_data['game_id']
        else:
            game_id = '33214'

        if 'game_name' in stream_data:
            game_name = stream_data['game_name']
        else:
            game_name = None

        if 'language' in stream_data:
            language = stream_data['language']
        else:
            language = None

        if 'started_at' in stream_data:
            started_at = stream_data['started_at']
        else:
            started_at = None

        if 'type' in stream_data:
            type = stream_data['type']
        else:
            type = None

        if 'viewer_count' in stream_data:
            viewer_count = stream_data['viewer_count']
        else:
            viewer_count = None

        if 'user_id' in stream_data:
            user_id = stream_data['user_id']
        else:
            user_id = '19571641'

        filtered_stream_data = {
        'id': id,
        'game_id': game_id,
        'game_name': game_name,
        'language': language,
        'started_at': started_at,
        'type': type,
        'viewer_count': viewer_count,
        'user_id': user_id
        }

        return filtered_stream_data


    def get_user_data(self, user_id_list):
        user_id = []
    
        for user_id in user_id_list:
            url = 'https://api.twitch.tv/kraken/users?_id={}'.format(user_id)
            header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
            'Accept': 'application/json'}

            userdata = requests.get(url, headers=header)
            ndata = userdata.json()

        return ndata

    def filter_user_data(self, user_data):
        
        if 'id' in user_data:
            id = user_data['id']
        else:
            id = '19571641' 

        if 'display_name' in user_data:
            display_name = user_data['display_name']
        else:
            display_name = None

        if 'type' in user_data:
            type = user_data['type']
        else:
            type = None

        if 'view_count' in user_data:
            view_count = user_data['view_count']
        else:
            view_count = None

        if 'follows' in user_data:
            follows = user_data['follows']
        else:
            follows = None
        
        filtered_user_data = {
        'id': id,
        'display_name': display_name,
        'type': type,
        'view_count': view_count,
        'follows': follows
        }

        return filtered_user_data


    def save_stream(self, game_list, stream_list):
        stream = Stream(
        id = stream_list['id'],
        game_id = game_list['id'],
        game_name = game_list['name'],
        language = stream_list['language'],
        started_at = stream_list['started_at'],
        type = stream_list['type'],
        viewer_count = stream_list['viewer_count'],
        user_id = stream_list['user_id']
        )

        stream.save()

        print('a stream do jogo {} foi salva '.format(stream.game_name)) 

    def save_user(self, user_list):
        user = User(
        id = user_list['id'],
        display_name = user_list['display_name'],
        type = user_list['type'],
        view_count = user_list['view_count'],
        follows = user_list['follows']
        )

        user.save()

        print('o user {} foi salvo'.format(user.id)) 
