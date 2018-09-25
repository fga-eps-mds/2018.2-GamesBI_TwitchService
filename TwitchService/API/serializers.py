from TwitchService.importdata.models import Stream, User, Game
from rest_framework import serializers

class GameSerializer(serializers.ModelSerializer):

	class Meta:

		model = Game
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = '__all__'


class StreamSerializer(serializers.ModelSerializer):

	game = GameSerializer()
	user = UserSerializer()

	class Meta:

		model = Stream
		fields = '__all__'
