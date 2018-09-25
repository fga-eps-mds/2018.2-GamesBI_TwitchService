import requests
import os
import time

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

        url = 'http://igdbweb:8000/api/get_igdb_games_list/name'
        header = {'Accept': 'application/json'}

        names_data = requests.get(url, headers=header)
        games_name = names_data.json()

        for game_name in games_name:
            game_data = self.get_game_data(game_name['name'])
            if not game_data['data']:
                continue
            filtered_game_data = self.filter_game_data(game_data['data'])
            stream_data = self.get_stream_data(filtered_game_data['id'])
            time.sleep(3)
            for stream in stream_data['data']:
                filtered_game_data['total_views'] = filtered_game_data['total_views'] + stream['viewer_count']
            self.save_game(filtered_game_data)
            for stream in stream_data['data']:
                filtered_stream_data = self.filter_stream_data(stream)
                filtered_user_data = self.get_user_data(stream['user_id'])
                self.save_user(filtered_user_data)
                self.save_stream(stream)
                time.sleep(3)

        return Response(data=games_name)

    def get_game_data(self, game_name):

        url = 'https://api.twitch.tv/helix/games?name={}'.format(game_name)
        header = {'Client-ID': 'nhnlqt9mgdmkf9ls184tt1nd753472',
        'Accept': 'application/json'}

        gamedata = requests.get(url, headers=header)
        ndata = gamedata.json()

        return ndata

    def filter_game_data(self, game_data):

        for data in game_data:
            if 'id' in data:
                id = data['id']
            else:
                id = None

            if 'name' in data:
                name = data['name']
            else:
                name = None

        filtered_game_data = {
        'id': id,
        'name': name,
        'total_views': 0
        }

        return filtered_game_data

    def get_stream_data(self, game_id):

        url =  'https://api.twitch.tv/helix/streams?game_id={}'.format(game_id)
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
            user_id = None

        filtered_stream_data = {
        'id': id,
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

        filtered_user_data = self.filter_user_data(ndata, followsdata)
        return filtered_user_data

    def filter_user_data(self, user_data, user_follows):

        if 'total' in user_follows:
            follows = user_follows['total']
        else:
            follows = None

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
                if posicao['type'] == "":
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
            'view_count': view_count,
            'follows': follows
            }

            return filtered_user_data

    def save_game(self, game_list):
        game = Game(
        game_id = game_list['id'],
        game_name = game_list['name'],
        total_views = game_list['total_views']
        )

        game.save()

        print('o jogo {} foi salvo '.format(game.game_name))
        print('id do jogo = {}'.format(game.game_id))
        print('a quantidade de views total do jogo = {}'.format(game.total_views))
        print('---')

    def save_stream(self, stream_list):
        stream = Stream(
        id = stream_list['id'],
        language = stream_list['language'],
        started_at = stream_list['started_at'],
        type = stream_list['type'],
        viewer_count = stream_list['viewer_count'],
        user_id = stream_list['user_id']
        )

        stream.save()

        print('id da stream = {}'.format(stream.id))
        print('linguagem da stream = {}'.format(stream.language))
        print('a stream foi iniciada em {}'.format(stream.started_at))
        print('tipo da stream = {}'.format(stream.type))
        print('a quantidade de views = {}'.format(stream.viewer_count))
        print('id do usuario = {}'.format(stream.user_id))
        print('---')

    def save_user(self, user_list):
        user = User(
        user_id = user_list['id'],
        display_name = user_list['display_name'],
        type = user_list['type'],
        view_count = user_list['view_count'],
        follows = user_list['follows']
        )

        user.save()

        print('o user {} foi salvo'.format(user.display_name))
        print('o id do usuario = {}'.format(user.id))
        print('o tipo = {}'.format(user.type))
        print('o numero de views = {}'.format(user.view_count))
        print('o numero de follows = {}'.format(user.follows))
        print(' ')
        print(' ')
