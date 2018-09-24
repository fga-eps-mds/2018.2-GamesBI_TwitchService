from TwitchService.importdata.models import Stream, User
from rest_framework import serializers

class StreamSerializer(serializers.ModelSerializer):

	class Meta:

		model = Stream
		fields = '__all__'
