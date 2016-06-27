from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from flask import request
import pygal
import os

import lyrics_to_words as ltw
#import numpy as np
import sqlite3
from model import predict_genre

dbname = 'Billboard_10yr.db'

wk_words = pd.read_csv('~/insight-data-science/words_by_week.csv',encoding='utf-8')
#import pysqlite

user = 'steeles' #add your username here (same as previous postgreSQL)                      
host = 'localhost'

db = create_engine('sqlite:///%s'%(dbname))
conn = None
conn = sqlite3.connect(dbname, check_same_thread=False);


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Dipity' },
       )

@app.route('/db')
def drake_page():
    sql_query = """                                                                       
                SELECT * FROM BB10yr WHERE artist LIKE 'Drake%';          
                """
    query_results = pd.read_sql_query(sql_query,conn)
    
    songs = ""
    for i in range(0,query_results.shape[0]):
        songs += query_results.iloc[i]['title']
        songs += "<br>"
    return songs


@app.route('/db_fancy')
def drake_page_fancy():
    sql_query = """                                                                       
                SELECT * FROM BB10yr WHERE artist LIKE 'Drake%';          
                """
    query_results = pd.read_sql_query(sql_query,conn)

    songs = []
    for i in range(0,query_results.shape[0]):
        songs.append(dict(date=query_results.iloc[i]['date'], 
            chart_name=query_results.iloc[i]['chart_name'], 
            title=query_results.iloc[i]['title'],
            artist=query_results.iloc[i]['artist']))
    return render_template('lyrics.html',songs=songs)



@app.route('/input')
def lyrics_input():
    return render_template("input.html")

@app.route('/output')
def lyrics_output():

    word=request.args.get('word')
    
    
    x=wk_words.date.tolist()

    terms = [ltw.lyrics_to_words(term) for term in word.strip().split()]
    
    y=[]
    for term in terms:
        y.append(wk_words[term].tolist())

    graph = pygal.Line(x_label_rotation=35,x_labels_major_every=6,show_minor_x_labels=False)
    graph.title= 'Performance of songs with %s on Billboard Hot 100!' % word
    graph.x_labels=x

    for i in xrange(len(y)):
        graph.add(terms[i],y[i])
    graph_data=graph.render_data_uri()

    # pull 'title' from input field and store it
    # song_title = request.args.get('title')
    # artist = request.args.get('artist')

    # if not artist:
    #     # now just pull out the ones the user selected
    #     query = "SELECT date, rank, chart_name, title, artist FROM BB10yr WHERE title LIKE '%s'" % ('%' + song_title + '%')
    #     print query
    #     #return query
    # else:
    #     query = "SELECT date, rank, chart_name, title, artist FROM BB10yr WHERE title LIKE '%s' and artist LIKE '%s'" % (song_title, artist + '%')
    #     print query
    #     #return query

    # query_results = pd.read_sql_query(query,conn)
    # print query_results
    # songs = []
    # if not query_results.empty:
    #     for i in range(0,query_results.shape[0]):
    #         songs.append(dict(date=query_results.iloc[i]['date'], 
    #             rank=query_results.iloc[i]['rank'],
    #             chart_name=query_results.iloc[i]['chart_name'], 
    #             title=query_results.iloc[i]['title'],
    #             artist=query_results.iloc[i]['artist']))
    #     the_result = 'foo'

    # title=song_title#query_results.iloc[0]['title']
    # #artist=query_results.iloc[0]['artist']
    # the_result = predict_genre(title,artist)
    return render_template("output.html", graph_data = graph_data)



