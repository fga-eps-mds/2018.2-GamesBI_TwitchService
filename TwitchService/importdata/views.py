import requests
import os
import time

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

        games_igdb = self.get_igdb_data()

        for game_name in games_name:

            game_data = self.get_game_data(game_igdb['name'])
            game_id = self.filter_game_data(game_data)
            #time.sleep(3000)
            if game_id == None:
                continue;
            stream_data = self.get_stream_data(game_id)
            print(stream_data)

            statistics = {
                'id': 
            }

            for stream in stream_data:
                filtered_stream_data = self.get_stream_data(game_id)
                user_data = get_user_data(self, filter_stream_data['user_id'])
                filtered_user_data = self.filter_user_data(user_data)

        return Response(data=games_name)

    def get_igdb_data(self):
        url = 'http://igdbweb:8000/api/get_igdb_games_list/name'
        header = {'Accept': 'application/json'}

        names_data = requests.get(url, headers=header)
        games_name = names_data.json()

        return games_name


    def get_game_data(self, game_name):

        url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        game_data = requests.get(url, headers=header).json()

        return game_data



    def filter_game_data(self, game_data):

        vetor_data = game_data['data']
        id = None
        for posicao in vetor_data:
            if 'id' in posicao:
                id = posicao['id']
            else:
                id = None

        return id

    def get_stream_data(self, game_id):

        url =  'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        stream_data = requests.get(url, headers=header).json()

        return stream_data


    def filter_stream_data(self, stream_data):

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

        return filtered_stream_data



    def get_user_data(self, user_id):

        #pegar dados do usuario
        time.sleep(3)
        url = 'https://api.twitch.tv/helix/users?id={}'.format(user_id)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        userdata = requests.get(url, headers=header)
        ndata = userdata.json()

        time.sleep(2)
        #pegar numero de follows do usuario
        url2 = 'https://api.twitch.tv/helix/users/follows?to_id={}'.format(user_id)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        userfollows = requests.get(url2, headers=header)
        followsdata = userfollows.json()



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
                if 'type' in posicao == "":
                    type = None
                else:
                    type = posicao['type']
            else:
                type = None

            if 'view_count' in posicao:
                view_count = posicao['view_count']
            else:
                view_count = None

            filtered_user_data = {
                'id': id,
                'display_name': display_name,
                'type': type,
                'view_count': view_count
            }

        return filtered_user_data

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

    def save_user(self, user_list, user_follows):
        user = User(
            id = user_list['id'],
            display_name = user_list['display_name'],
            type = user_list['type'],
            view_count = user_list['view_count'],
            follows = user_follows['total']
        )

        user.save()

        print('o user {} foi salvo'.format(user.display_name))
        print('o id do usuario = {}'.format(user.id))
        print('o tipo = {}'.format(user.type))
        print('o numero de views = {}'.format(user.view_count))
        print('o numero de follows = {}'.format(user.follows))
        print(' ')
        print(' ')
