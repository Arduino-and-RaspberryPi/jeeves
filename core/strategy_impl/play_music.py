from .base_strategy import BaseStrategy
from utils.say import say
from utils.user_input import user_input

import subprocess
import spotipy


class PlayMusic(BaseStrategy):
    def __init__(self):
        self.type = "s/w"
        self.artist = None
        self.sp = spotipy.Spotify()
        self.sp.trace = False

    def describe(self):
        return "Would you like to listen to some music?"

    def find_artist(self, name):
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            self.artist = items[0]
            say("Curating the best from %s..." % self.artist['name'])
            return True

        return False

    def start_spotify(self):
        running = int(subprocess.check_output([
            'osascript',
            '-e', 'tell application "System Events"',
            '-e', 'count (every process whose name is "Spotify")',
            '-e', 'end tell'
        ]).strip())

        if not running:
            subprocess.call([
                'osascript',
                '-e',
                'tell application "Spotify" to activate'
            ])

    def get_top_tracks(self):
        tracks = self.sp.artist_top_tracks(self.artist["uri"])['tracks']
        if len(tracks) > 0:
            say("Here's what I think are their best works.")
            count = 0

            playlist = {}

            for track in tracks:
                print("[%d] Song: %s Album: %s" % (count + 1, track['name'], track['album']['name']))
                say("%s from the album %s" % (track['name'], track['album']['name']))
                count += 1

                playlist[str(count)] = (self.artist['name'], track['name'], track['album']['name'], track['uri'])

            say("Please type the index of the song you would like to hear")
            choice = user_input("reply: ")

            say("Playing %s from the album %s." % (playlist[choice][1], playlist[choice][2]))

            subprocess.call([
                'osascript',
                '-e',
                'tell app "Spotify" to play track "%s"' % playlist[choice][3]
            ])
        else:
            say("Sorry, Although I know %s but I can't find any songs. Weird" % (self.artist['name']))

    def perform(self):
        self.start_spotify()
        say("Please type the artist you want to hear: ")
        name = user_input("reply: ")

        if not self.find_artist(name):
            say("That's weird. All this knowledge and still I couldn't find anything. I'll try to learn more.")
            say("My sincere apologies for that.")
            return

        self.get_top_tracks()

    def react(self):
        say("Okay, lets find some awesome music just for you...")
