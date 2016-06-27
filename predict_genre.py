'''bag of word features'''

import get_song_lyrics
import lyrics_to_bow
import re

def predict_genre(song_title,artist=None):
	# check if we already have the lryics
	#dfLyricBow=
	#if 
	lyrics, title, url = get_song_lyrics(song_title,artist)

	print 'Are these the right lyrics? \n %s' % (lyrics)

	bow = lyrics_to_bow(lyrics)

	