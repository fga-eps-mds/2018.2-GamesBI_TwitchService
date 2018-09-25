from TwitchService.importdata.models import Stream, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = '__all__'


class StreamSerializer(serializers.ModelSerializer):

	user = UserSerializer()

	class Meta:

		model = Stream
		fields = '__all__'