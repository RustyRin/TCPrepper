'''
This file downloads the top N clips from the Twitch category of X in Y timeframe
'''
from itertools import islice
from twitch import TwitchHelix
from datetime import datetime, date, timedelta
import youtube_dl

# Options
download_top_game_clips = True      # go through the top clips of a game and download them
game_ID = 488552                    # the twitch game ID that you want to get clips from
number_of_clips_to_download = 1     # the number of clips you want
clips_from_days_ago = 1             # get clips that were made how many days ago. 1 means you're getting clips from yesterday, 7 means last week

download_clips_from_list = True     # download clip urls from download_list.txt, clips should be one per line in the file

overlay_channel_name = True         # apply twitch channel name on top of the video
overlay_channel_profile_pic = True  # apply twitch channel profile picture on top of the video
overlay_clipchimp_name = True       # apply twitch name of the person that made the clip 


ydl_opts = {
    'outtmpl': 'download/%(title)s.%(ext)s',
    'quiet': True,
    'simulate': True
}

with open('twitch_clientID.txt') as f:
    twitch_clientID = f.readline().rstrip()

client = TwitchHelix(client_id=twitch_clientID)
yesterday_date = (datetime.now()-timedelta(days=clips_from_days_ago)).strftime('%Y-%m-%dT00:00:00Z')
clip_iterator = client.get_clips(game_id=game_ID, started_at=yesterday_date)
for x in islice(clip_iterator, 0, number_of_clips_to_download):
    print('---------------------------------------')
    print('Twitch Channel: ' + x.broadcaster_name)
    print('Clip Title: \t' + x.title)
    print('Clip Chimp: \t' + x.creator_name)
    print('Clip URL: \t' + x.url)

    print('Downloading Clip...')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([x.embed_url])
    print('Complete!')
