from django.db import models

class User(models.Model):
	user_name = models.CharField(max_length=255)

class Track(models.Model):
	title = models.CharField(max_length=255)
	speaker = models.CharField(max_length=255)
	duration = models.IntegerField()
	permalink_url = models.CharField(max_length=255)

class Comment(models.Model):
	user = models.ForeignKey(User)
	timestamp = models.IntegerField()
	track = models.ForeignKey(Track)
	comment_url = models.CharField(max_length=255)

class Keyword(models.Model):
	keyword = models.CharField(max_length=255)
	comment = models.ForeignKey(Comment)



