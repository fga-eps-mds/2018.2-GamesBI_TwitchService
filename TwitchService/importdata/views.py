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

        games_name = ['fortnite','The walking dead']
        '''
        url = 'http://localhost:8000/get_igdb_games_list/Name'
        header = {'Accept': 'application/json'}

        names_data = requests.get(url, headers=header)
        games_name = names_data.json()
        '''

        for game_name in games_name:
            self.get_game_data(game_name)

        '''
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
        print('-------------------------------------')
        users = User.objects.all()
        for user in users:
            print(user.id)
            print(user.display_name)
            print(user.type)
            print(user.view_count)
            print(user.follows)

            print('------------')
        '''

        return Response(data=games_name)

    def get_game_data(self, game_name):

        url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        gamedata = requests.get(url, headers=header)
        ndata = gamedata.json()

        self.filter_game_data(ndata)

    def filter_game_data(self, game_data):

        vetor_data = game_data['data']

        for posicao in vetor_data:
            if 'id' in posicao:
                id = posicao['id']
            else:
                id = None

            if 'name' in posicao:
                name = posicao['name']
            else:
                name = None

            filtered_game_data = {
            'id': id,
            'name': name
            }

            self.get_stream_data(filtered_game_data['id'], filtered_game_data)  

    def get_stream_data(self, game_id, filtered_game_data):

        url =  'https://api.twitch.tv/helix/streams?id={}'.format(game_id)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        streamdata = requests.get(url, headers=header)
        ndata = streamdata.json() 

        self.filter_stream_data(ndata, filtered_game_data)


    def filter_stream_data(self, stream_data, filtered_game_data):

        vetor_data = stream_data['data']

        for posicao in vetor_data:
            if 'id' in posicao:
                id = posicao['id']
            else:
                id = None

            if 'game_id' in posicao:
                game_id = posicao['game_id']
            else:
                game_id = None

            if 'language' in posicao:
                language = posicao['language']
            else:
                language = None

            if 'started_at' in posicao:
                started_at = posicao['started_at']
            else:
                started_at = None

            if 'type' in posicao:
                type = posicao['type']
            else:
                type = None

            if 'viewer_count' in posicao:
                viewer_count = posicao['viewer_count']
            else:
                viewer_count = None

            if 'user_id' in posicao:
                user_id = posicao['user_id']
            else:
                user_id = None

            filtered_stream_data = {
            'id': id,
            'game_id': game_id,
            'language': language,
            'started_at': started_at,
            'type': type,
            'viewer_count': viewer_count,
            'user_id': user_id
            }

            self.save_stream(filtered_stream_data, filtered_game_data)

            self.get_user_data(filtered_stream_data['user_id'])

    def get_user_data(self, user_id):

        url = 'https://api.twitch.tv/helix/users?id={}'.format(user_id)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        userdata = requests.get(url, headers=header)
        ndata = userdata.json()

        self.filter_user_data(ndata)

    def filter_user_data(self, user_data):

        vetor_data = user_data['data']

        for posicao in vetor_data:
            if 'id' in posicao:
                id = posicao['id']
            else:
                id = None 

            if 'display_name' in posicao:
                display_name = posicao['display_name']
            else:
                display_name = None

            if 'type' in posicao:
                type = posicao['type']
            else:
                type = None

            if 'view_count' in posicao:
                view_count = posicao['view_count']
            else:
                view_count = None

            if 'follows' in posicao:
                follows = posicao['follows']
            else:
                follows = None
            
            filtered_user_data = {
            'id': id,
            'display_name': display_name,
            'type': type,
            'view_count': view_count,
            'follows': follows
            }

            self.save_user(filtered_user_data)


    def save_stream(self, stream_list, game_list):
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
        print('id da stream = {}'.format(stream.id))
        print('id do jogo = {}'.format(stream.game_id))
        print('nome do jogo = {}'.format(stream.game_name))
        print('linguagem da stream = {}'.format(stream.language))
        print('a stream foi iniciada em {}'.format(stream.started_at))
        print('tipo da stream = {}'.format(stream.type))
        print('a quantidade de views = {}'.format(stream.viewer_count))
        print('id do usuario = {}'.format(stream.user_id))
        print('---')

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
        print('o display usado = {}'.format(user.display_name))
        print('o tipo = {}'.format(user.type))
        print('o numero de views = {}'.format(user.view_count))
        print('o numero de follows = {}'.format(user.follows))
        print(' ')
        print(' ')  