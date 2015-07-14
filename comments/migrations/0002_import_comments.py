# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

from yeg_oral_history import settings
import soundcloud

class CommentMigrator:
	def migrate(self, apps, schema_editor):
		User = apps.get_model('comments', 'User')
		Track = apps.get_model('comments', 'Track')
		Comment = apps.get_model('comments', 'Comment')
		Keyword = apps.get_model('comments', 'Keyword')

		client = soundcloud.Client(client_id=settings.CLIENT_ID)

		openedmonton_user = client.get('/resolve', url='http://soundcloud.com/openedmonton')
		openedmonton_user_id = openedmonton_user.id

		playlists = client.get('/users/%s/playlists' % (openedmonton_user_id,))
		openedmonton_playlists = filter(lambda playlist: playlist.title == settings.ORAL_HISTORY_PLAYLIST_NAME, playlists)
		oral_history_playlist = openedmonton_playlists[0]

		presentation_track_ids = [track['id'] for track in oral_history_playlist.tracks]

		for track_id in presentation_track_ids:
			comments = client.get('/tracks/%s/comments' % track_id)
			track = client.get('/tracks/%s' % track_id)

			ourTrack, created = Track.objects.get_or_create(
				title=track.title,
				speaker=self.__extract_speaker_name(track.title),
				duration=track.duration, 
				permalink_url=track.permalink_url)

			for comment in comments:
				user, created = User.objects.get_or_create(user_name=comment.user['username'])

				ourComment = Comment(
					user=user, 
					track=ourTrack, 
					timestamp=comment.timestamp,
					comment_url=self.__create_comment_url(ourTrack.permalink_url, comment.timestamp))

				ourComment.save()

				self.__extract_keywords(comment, ourComment, Keyword)

	def roll_back(self, apps, schema_editor):
		User = apps.get_model('comments', 'User')
		Track = apps.get_model('comments', 'Track')
		Comment = apps.get_model('comments', 'Comment')
		Keyword = apps.get_model('comments', 'Keyword')

		Keyword.objects.all().delete()
		Comment.objects.all().delete()
		Track.objects.all().delete()
		User.objects.all().delete()

	def __extract_keywords(self, commentSoundCloud, commentDjango, keywordModel):
		keywords = map(lambda keywordPhrase: keywordPhrase.strip(), commentSoundCloud.body.split(','))

		for keyword in keywords:
			keyword = keywordModel(keyword=keyword, comment=commentDjango)
			keyword.save()

	def __create_comment_url(self, permalink_url, timestamp):
		timestamp = int(timestamp)

		minutes = (timestamp / 1000)  / 60;
		seconds = (timestamp / 1000) % 60;

		return "%s#t=%sm%ss" % (permalink_url, minutes, seconds)

	def __extract_speaker_name(self, track_title):
		tokens = track_title.split(' ')

		# 1 word track titles
		if len(tokens) == 1:
			return tokens[0]
		# "Mike - 2015 - 04 - 29,5.21 PM"-esce titles
		elif len(tokens) > 1:
			if tokens[1] == '-':
				return tokens[0]
			elif len(tokens[1]) == 1 or len(tokens[1]) == 2:
				return " ".join(tokens[0:2])
			elif tokens[1] == 'And' or tokens[1] == 'with':
				return " ".join(tokens[0:3])
			elif tokens[1] == 'March' or tokens[1] == 'April':
				return tokens[0]
			else:
				return ""
		else:
			return ""
			

commentMigrator = CommentMigrator()

class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(commentMigrator.migrate, commentMigrator.roll_back)
    ]
