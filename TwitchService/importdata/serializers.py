from .models import Stream, User
from rest_framework import serializers

class StreamSerializer(serializers.ModelSerializer):

	class Meta:

		model = Stream
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

	class Meta:

		model = User
		fields = '__all__'
