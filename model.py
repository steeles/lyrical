'''bag of word features'''

import get_song_lyricsProx as gsl
#import word_fq_dist	
import lyrics_to_bow as lb
import re
import pandas as pd 
import numpy as np
from sklearn.externals import joblib

def predict_genre(song_title,artist=None):
	# check if we already have the lryics
	#dfLyricBow=
	#if 
	lyrics, title, url = gsl.get_song_lyricsProx(song_title,artist)
	
	if isinstance(lyrics,basestring):
		bow = lb.lyrics_to_bow(lyrics)
		#return title + lyrics
		features = create_features(bow)
		tfidfv = joblib.load('pkldir/tfidf_txf.pkl')

		tfFeatures = tfidfv.transform(features)
		furrest = joblib.load('pkldir/forest785.pkl')
		prediction = furrest.predict(tfFeatures)

		return prediction + title + lyrics 


	elif np.isnan(lyrics):
		return 'Couldn\'t find the lyrics.'
		#print 'Are these the right lyrics? \n %s' % (lyrics)
	else:
		return '...nothing'
		

def create_features(bow,vpath='./mxm_10yrWords.csv'):
	words = pd.read_csv(vpath,header=None,encoding='utf-8')
	wordSeries= words[0]
	counts = np.zeros(len(words))
	
	for word,count in bow.iteritems():
	    msk = wordSeries == word
	    entry = wordSeries[msk]
	    print entry
	    if msk.any():
	        ind = np.where(msk)
	        counts[ind]=count

	features = counts.transpose()

	return features


		

