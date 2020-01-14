'''
This file downloads the top N clips from the Twitch category of X in Y timeframe
'''
from itertools import islice
from twitch import TwitchHelix
from datetime import datetime, date, timedelta
import youtube_dl

ydl_opts = {
    'outtmpl': 'download/%(title)s.%(ext)s',
    'quiet': True,
    'simulate': True
}

with open('twitch_clientID.txt') as f:
    twitch_clientID = f.readline().rstrip()

client = TwitchHelix(client_id=twitch_clientID)
#print((datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d-T00:00:00Z'))
yesterday_date = (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z')
clip_iterator = client.get_clips(game_id='488552', started_at=yesterday_date)
#streams_iterator = client.get_streams(page_size=100)
for x in islice(clip_iterator, 0, 1):
    print('---------------------------------------')
    print('Twitch Channel: ' + x.broadcaster_name)
    print('Clip Title: \t' + x.title)
    print('Clip Chimp: \t' + x.creator_name)
    print('Clip URL: \t' + x.url)

    print('Downloading Clip...')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([x.embed_url])
    print('Complete!')
