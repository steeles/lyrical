'''function to get all the unique lyrics from a billboard data frame.
I probably want date of peak position, title, artist, best chart, peak position
for my learning model'''

import pandas as pd
import numpy as np
from time import sleep
import get_song_lyricsProx as gsl
import pdb
import csv

def build_lyric_db(df_BB,l_df=None,saveloc='lyrics_BB.csv',Append=True): # maybe input the csv file?
	
	if saveloc:
		if Append:
			f = csv.writer(open(saveloc,"awb+",0))
		else:
			f = csv.writer(open(saveloc,"wb+",0))
		f.writerow(['date','title','artist','lyrics','chart_name','peakPos','url'])

		idx={
		 
		'date' : 0,
		'title' : 1,
		'artist' : 2,
		'lyrics' : 3, 
		'chart_name' : 4,
		'peakPos' : 5,
		'url' : 6
		}

	
	ordered_songs = df_BB.groupby('title',group_keys=False,as_index=False).apply(lambda x: 
	        x.ix[x.peakPos.idxmin()])

	unique_songs = ordered_songs[['date','title','artist','chart_name','peakPos']].drop_duplicates(subset=['title','artist'])
	
	idx = unique_songs.index
	unique_songs['lyrics']=np.nan
	unique_songs['url']=np.nan
	unique_songs.reset_index(drop=True,inplace=True)
	#unique_songs.index = 


	for title, artist, index in zip(unique_songs['title'],unique_songs['artist'],unique_songs.index):

		try:
			lyrics, titleEff, url = gsl.get_song_lyricsProx(title,artist)
			lyrics.encode('utf-8')
			titleEff.encode('utf-8')
			
		except:
			continue#print lyrics
		lyrics.encode('utf-8')
		row =unique_songs.iloc[int(index)]
		# load it into the list
		if saveloc:
			try:
				f.writerow([row.date, row.title, row.artist, lyrics, row.chart_name, row.peakPos, url])
			except:
				print 'something funky happened! '
				print lyrics
		unique_songs.loc[index,'lyrics'] = lyrics
		unique_songs.loc[index,'url'] = url
		sleep(90)
		#pdb.set_trace()
	return unique_songs

