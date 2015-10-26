SELECT
	ct.title AS track_title
	,ct.speaker AS track_speaker
	,ct.duration AS track_duration
	,cc.timestamp AS comment_timestamp
	,cc.comment_url AS comment_url
	,cu.user_name AS comment_commenter_username
	,ck.keyword AS comment_keyword
FROM
	comments_track ct 
	INNER JOIN comments_comment cc
		ON ct.id = cc.track_id
	INNER JOIN comments_user cu
		ON cc.user_id = cu.id
	INNER JOIN comments_keyword ck
		ON cc.id = ck.comment_id
	