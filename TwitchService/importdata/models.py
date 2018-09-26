from django.db import models

class Game(models.Model):

	game_id = models.IntegerField(
		('Game ID'),
		help_text=("Id do jogo na Twitch"),
		primary_key=True
	)

	game_name = models.CharField(
		('Game name'),
		help_text=("Name of game"),
		max_length=100,
		null=True
	)

	total_views = models.IntegerField(
		('Total views'),
		help_text=("Total views of a game"),
		null=True
	)


class User(models.Model):

	user_id = models.IntegerField(
		('User ID'),
		help_text=("User id at Twitch API"),
		primary_key=True
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
		primary_key=True
	)

	language = models.CharField(
		('Language'),
		help_text=("Language of stream"),
		max_length=100,
		null=True
	)

	started_at = models.CharField(
		('Started date'),
		help_text=("Date when stream started"),
		max_length=100,
		null=True
	)

	type = models.CharField(
		('Type'),
		help_text=("Type of stream"),
		max_length=100,
		null=True
	)

	viewer_count = models.IntegerField(
		('Viewer count'),
		help_text=("Number of views in stream"),
		null=True
	)

	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)

	game = models.ForeignKey(
		Game,
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
