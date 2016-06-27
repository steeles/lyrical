from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from flask import request
#import numpy as np
import sqlite3

dbname = 'lyrics-billboardDB.db'


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
                SELECT * FROM lyrics_billboard WHERE artist LIKE 'Drake%';          
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
                SELECT * FROM lyrics_billboard WHERE artist LIKE 'Drake%';          
                """
    query_results = pd.read_sql_query(sql_query,conn)

    songs = []
    for i in range(0,query_results.shape[0]):
        songs.append(dict(id=query_results.iloc[i]['id'], 
            chart_name=query_results.iloc[i]['chart_name'], 
            title=query_results.iloc[i]['title']))
    return render_template('lyrics.html',songs=songs)



@app.route('/input')
def lyrics_input():
    return render_template("input.html")

@app.route('/output')
def lyrics_output():
    # pull 'title' from input field and store it
    song_title = request.args.get('title')
    # now just pull out the ones the user selected
    query = "SELECT id, chart_name, title FROM lyrics_billboard WHERE artist='Drake' AND title='%s'" % song_title
    print query
    query_results = pd.read_sql_query(query,conn)
    print query_results
    songs = []
    for i in range(0,query_results.shape[0]):
        songs.append(dict(id=query_results.iloc[i]['id'], 
            chart_name=query_results.iloc[i]['chart_name'], 
            title=query_results.iloc[i]['title']))
    the_result = 'foo'

    return render_template("output.html", songs = songs, the_result = the_result)



