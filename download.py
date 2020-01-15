'''
This file downloads the top N clips from the Twitch category of X in Y timeframe
'''
from itertools import islice
from twitch import TwitchHelix
from datetime import datetime, date, timedelta
from moviepy.editor import *
import youtube_dl
import json
import urllib.request
import os

# Options
download_top_game_clips = True      # go through the top clips of a game and download them
game_ID = 488552                    # the twitch game ID that you want to get clips from
number_of_clips_to_download = 5     # the number of clips you want
clips_from_days_ago = 1             # get clips that were made how many days ago. 1 means you're getting clips from yesterday, 7 means last week

download_clips_from_list = True     # download clip urls from download_list.txt, clips should be one per line in the file

overlay_channel_name = True         # apply twitch channel name on top of the video
overlay_channel_profile_pic = True  # apply twitch channel profile picture on top of the video
overlay_clip_title = True           # show the clip title
overlay_clipchimp_name = True       # apply twitch name of the person that made the clip
overlay_font = 'Dyuthi'             # font that the overlay will be in
overlay_align = 'north-west'        # where the overlay will be anchored. See https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#textclip align for more options
overlay_text_color = 'white'        # color of the text in the overlay
overlay_stroke_color = 'black'      # color of the stroke around the overlay text
overlay_stroke_width = 1            # size of the stroke. 0 for no stroke, can also be a float number like 1.5
overlay_channel_name_size = 75      # size of the channel name text. the rest of the overlay is anchored to this size and will adjust to this

ydl_opts = {
    'outtmpl': 'download/clips/%(title)s.%(ext)s'.strip('[?<>:\"\\/|*]'),
    'quiet': True,
    'simulate': False
}

with open('twitch_clientID.txt') as f:
    twitch_clientID = f.readline().rstrip()

client = TwitchHelix(client_id=twitch_clientID)
yesterday_date = (datetime.now()-timedelta(days=clips_from_days_ago)).strftime('%Y-%m-%dT00:00:00Z')
clip_array = []

if download_top_game_clips:
    clip_iterator = client.get_clips(game_id=game_ID, started_at=yesterday_date)
    for clip in islice(clip_iterator, 0, number_of_clips_to_download):

        print('---------------------------------------')
        print('Twitch Channel: ' + clip.broadcaster_name + ' (' + clip.broadcaster_id + ')')
        print('Clip Title: \t' + clip.title + ' (' + clip.id + ')')
        print('Clip Chimp: \t' + clip.creator_name)
        print('Clip URL: \t' + clip.url)

        ydl_opts = {
            'outtmpl': 'download/clips/' + clip.id + '.%(ext)s'.strip('[?<>:\"\\/|*]'),
            'quiet': True,
            'simulate': False
        }

        print('Downloading Clip...')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([clip.embed_url])
        print('Complete!')

        tc_video = VideoFileClip('download/clips/' + clip.id.strip('[?<>:"\\/|?*]') + '.mp4', target_resolution=(1080,1920))
        tc_channel = None
        tc_pfp = None
        tc_title = None
        tc_chimp = None

        if overlay_channel_name:
            print('Making channel name text clip...')
            tc_channel = TextClip(txt=clip.broadcaster_name, fontsize=overlay_channel_name_size, color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='caption', font=overlay_font)
            tc_channel = tc_channel.set_position((.04, 'top'), relative=True)

        if overlay_channel_profile_pic:
            print('Downloading channel profile picture...')
            url = 'https://api.twitch.tv/helix/users?id=' + clip.broadcaster_id
            req = urllib.request.Request(url)
            req.add_header("Client-ID", twitch_clientID)
            resp = urllib.request.urlopen(req)
            data = resp
            xjson = json.load(data)["data"][0]
            urllib.request.urlretrieve(xjson["profile_image_url"], 'download/pfp/' + clip.broadcaster_id + '.png')

            print('Making channel profile picture image clip...')
            tc_pfp = ImageClip('download/pfp/' + clip.broadcaster_id + '.png')
            tc_pfp = tc_pfp.resize(height=overlay_channel_name_size + (overlay_channel_name_size/2.8))
            tc_pfp = tc_pfp.set_position((.005, .02), relative = True)
            tc_channel = tc_channel.set_position((.06, 'top'), relative=True)

        if overlay_clip_title:
            print('Making video title clip...')
            tc_title = TextClip(txt=clip.title, fontsize=(overlay_channel_name_size/2.4), color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='label', font=overlay_font)
            tc_title = tc_title.set_position((.06, .067), relative = True)

        if overlay_clipchimp_name:
            print('Making clip chimp text clip...')
            tc_chimp = TextClip(txt=('Clipped by: ' + clip.creator_name), fontsize=(overlay_channel_name_size/3.5), color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='label', font=overlay_font)
            if overlay_clip_title:
                tc_chimp = tc_chimp.set_position((.06, .09), relative = True)
            else:
                tc_chimp = tc_chimp.set_position((.06, .067), relative = True)

        clip_array.append(tc_video)
        clip_array.append(tc_channel)
        clip_array.append(tc_pfp)
        clip_array.append(tc_title)
        clip_array.append(tc_chimp)



        render = CompositeVideoClip(clip_array).set_duration(tc_video.duration)
        render.write_videofile('export/' + clip.id.strip('[?<>:"\\/|?*]') + '.mp4', fps=60, threads = 4)

        clip_array = []

if download_clips_from_list:
    with open('download_list.txt') as f:
        for line in f:
            #print(line.rstrip('\n').split('/')[5])
            clip = client.get_clips(clip_ids=line.rstrip('\n').split('/')[5])[0]

            print('---------------------------------------')
            print('Twitch Channel: ' + clip.broadcaster_name + ' (' + clip.broadcaster_id + ')')
            print('Clip Title: \t' + clip.title)
            print('Clip Chimp: \t' + clip.creator_name)
            print('Clip URL: \t' + clip.url)

            ydl_opts = {
                'outtmpl': 'download/clips/' + clip.id + '.%(ext)s'.strip('[?<>:\"\\/|*]'),
                'quiet': True,
                'simulate': False
            }

            print('Downloading Clip...')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([clip.embed_url])
            print('Complete!')

            tc_video = VideoFileClip('download/clips/' + clip.id + '.mp4', target_resolution=(1080,1920))
            tc_channel = None
            tc_pfp = None
            tc_title = None
            tc_chimp = None

            if overlay_channel_name:
                print('Making channel name text clip...')
                tc_channel = TextClip(txt=clip.broadcaster_name, fontsize=overlay_channel_name_size, color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='caption', font=overlay_font)
                tc_channel = tc_channel.set_position((.04, 'top'), relative=True)

            if overlay_channel_profile_pic:
                print('Downloading channel profile picture...')
                url = 'https://api.twitch.tv/helix/users?id=' + clip.broadcaster_id
                req = urllib.request.Request(url)
                req.add_header("Client-ID", twitch_clientID)
                resp = urllib.request.urlopen(req)
                data = resp
                xjson = json.load(data)["data"][0]
                urllib.request.urlretrieve(xjson["profile_image_url"], 'download/pfp/' + clip.broadcaster_id + '.png')

                print('Making channel profile picture image clip...')
                tc_pfp = ImageClip('download/pfp/' + clip.broadcaster_id + '.png')
                tc_pfp = tc_pfp.resize(height=overlay_channel_name_size + (overlay_channel_name_size/2.8))
                tc_pfp = tc_pfp.set_position((.005, .02), relative = True)
                tc_channel = tc_channel.set_position((.06, 'top'), relative=True)

            if overlay_clip_title:
                print('Making video title clip...')
                tc_title = TextClip(txt=clip.title, fontsize=(overlay_channel_name_size/2.4), color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='label', font=overlay_font)
                tc_title = tc_title.set_position((.06, .067), relative = True)

            if overlay_clipchimp_name:
                print('Making clip chimp text clip...')
                tc_chimp = TextClip(txt=('Clipped by: ' + clip.creator_name), fontsize=(overlay_channel_name_size/3.5), color=overlay_text_color, stroke_width=overlay_stroke_width, stroke_color=overlay_stroke_color, align=overlay_align, method='label', font=overlay_font)
                if overlay_clip_title:
                    tc_chimp = tc_chimp.set_position((.06, .09), relative = True)
                else:
                    tc_chimp = tc_chimp.set_position((.06, .067), relative = True)

            clip_array.append(tc_video)
            clip_array.append(tc_channel)
            clip_array.append(tc_pfp)
            clip_array.append(tc_title)
            clip_array.append(tc_chimp)



            render = CompositeVideoClip(clip_array).set_duration(tc_video.duration)
            render.write_videofile('export/' + clip.id + '.mp4', fps=60, threads = 4)

            clip_array = []
