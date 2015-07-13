# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

import soundcloud
import settings

class CommentMigrator:
	def migrate(self):
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

			for comment in comments:
				user = User.objects.get_or_create(user_name=comment.user['username'])

				ourComment = Comment(user=user, timestamp=comment.timestamp)
				ourComment.save()

				self.__extract_keywords(comment, ourComment, Keyword)

	def roll_back(self):
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

commentMigrator = CommentMigrator()

class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(commentMigrator.migrate, commentMigrator.roll_back)
    ]
