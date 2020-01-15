# TCPrepper
Helps automate the editing process of Twitch clip YouTube channels by offloading repetitive tasks

For the time being, the python-twitch-client api still doesn't support some new parameters from Twitch. So to automatically download the top clips of the day you are going to have to edit the api.
1. Open a terminal and enter `pip show python-twitch-client` then look for the location. For me it is `~/.local/lib/python3.7/site-packages` on Ubuntu
2. Inside the site-packages folder there is a `twitch` folder, open it
3. Now open `helix`
4. Open `api.py` in whatever text editor you prefer
5. Line 75 is where the function we are going to edit is.
6. In the args of `get_clips` add `, ended_at=None, started_at=None`
7. Then on line 87 there is the params box. Replace it with

```
params = {
    'broadcaster_id': broadcaster_id,
    'game_id': game_id,
    'id': clip_ids,
    'after': after,
    'before': before,
    'ended_at': ended_at,
    'started_at': started_at,
}
```
8. Save


## Setting Up
1. Download dependencies
    - [python-twitch-client](https://github.com/tsifrer/python-twitch-client) For downloading the top twitch clips
        - For the time being, the python-twitch-client api still doesn't support some new parameters from Twitch. So to automatically download the top clips of the day you are going to have to edit the api.
            1. Open a terminal and enter `pip show python-twitch-client` then look for the location. For me it is `~/.local/lib/python3.7/site-packages` on Ubuntu
            2. Inside the site-packages folder there is a `twitch` folder, open it
            3. Now open `helix`
            4. Open `api.py` in whatever text editor you prefer
            5. Line 75 is where the function we are going to edit is.
            6. In the args of `get_clips` add `, ended_at=None, started_at=None`
            7. Then on line 87 there is the params box. Replace it with
                 ```
                params = {
                    'broadcaster_id': broadcaster_id,
                    'game_id': game_id,
                    'id': clip_ids,
                    'after': after,
                    'before': before,
                    'ended_at': ended_at,
                    'started_at': started_at,
                }
                ```
            8. Save
    - [moviepy](https://github.com/Zulko/moviepy) for editing and overlay
    - [youtube-dl](https://github.com/ytdl-org/youtube-dl) for downloading videos
    - [Imagemagick](https://imagemagick.org/index.php) for the text overlay
2. Follow the instructions [here](https://dev.twitch.tv/docs/api#step-1-setup) on how to register an application on Twitch to get your
3. Edit settings
    - Most are self explanitory, but you might have to change the font. You can see the available fonts dun the `list_fonts.py` in the debug folder and change it to one of those listed

### Todo
- [ ] Clean up program
- [ ] Actually use functions
- [ ] Allow parts or all of the overlay to fade away over time
- [ ] Concatenate export into one long video
