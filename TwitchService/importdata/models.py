from django.db import models

class User(models.Model):

	id = models.IntegerField(
		('User ID'),
		help_text=("User id at Twitch API"),
		primary_key=True,
	)

	display_name = models.CharField(
		('Display name'),
		help_text=("Display name"),
		max_length=100,
		null=True
	)

	type = models.CharField(
		('Type'),
		help_text=("Type"),
		max_length=100,
		null=True
	)

	view_count = models.IntegerField(
		('Count views'),
		help_text=("Views couting of user"),
		null=True
	)

	follows = models.IntegerField(
		('follows'),
		help_text=("Number of followers"),
		null=True
	)		
	

class Stream(models.Model):

	id = models.IntegerField(
		('Stream ID'),
		help_text=("Id da stream na Twitch"),
		primary_key=True,
	)

	game_id = models.IntegerField(
		('Game ID'),
		help_text=("Id do jogo na Twitch")
	)

	game_name = models.CharField(
		('Name'),
		help_text=("Name of game"),
		max_length=100,
		null=True
	)

	language = models.CharField(
		('Language'),
		help_text=("Language of stream"),
		max_length=100,
		null=True
	)

	started_at = models.DateField(
		('Started date'),
		help_text=("Date when stream started"),
		null=True
	)

	type = models.CharField(
		('Type'),
		help_text=("Type of stream"),
		max_length=100,
		null=True
	)

	viewer_count = models.FloatField(
		('Viewer count'),
		help_text=("Number of views in stream"),
		max_length=100,
		null=True
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)

	def __str__(self):
	    """
	    Returns the object as a string, the attribute that will represent
	    the object.
	    """

	    return self.name

	class Meta:
	    """
	    Some information about feedback class.
	    """
	    verbose_name = ("Twitch Game")
	    verbose_name_plural = ("Twitch Games")
