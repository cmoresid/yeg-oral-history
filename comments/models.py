from django.db import models

class User(models.Model):
	user_name = models.CharField(max_length=255)

class Track(models.Model):
	title = models.CharField(max_length=255)
	duration = models.IntegerField()

class Comment(models.Model):
	user = models.ForeignKey(User)
	timestamp = models.IntegerField()

class Keyword(models.Model):
	keyword = models.CharField(max_length=255)
	comment = models.ForeignKey(Comment)



