import requests
from flask import Flask, render_template, Response,request
import sys
import mysql.connector
import os
from werkzeug.utils import secure_filename
from mysql.connector import connection

connection = mysql.connector.connect(host='sql6.freemysqlhosting.net',
                                             database='sql6425987',
                                             user=' sql6425987',
                                             password='by6bccuNLw')
#Getting songs from Db
def return_dict():

    try:

        cursor = connection.cursor()
        query = " select * from songs;"
        result = cursor.execute(query)
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in cursor.fetchall()]


        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to fetch MySQL table {}".format(error))

    """finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")"""
    print(data)
    return data

# Initialize Flask.
app = Flask(__name__, static_url_path="/static")


#Route to render GUI
@app.route('/')
def show_entries():
    stream_entries = return_dict()
    return render_template('index.html', entries=stream_entries)
#Route to render to Upload Page
@app.route('/uploadfiles')
def uploadfile():
    return render_template("upload.html")

#Route to render after Upload
@app.route('/upload',methods=["GET","POST"])
def upload():
    UPLOAD_SONG='D:\downloads\\flask-music-streaming-master\\flask-music-streaming-master\static\\music'
    app.config['UPLOAD_SONG'] = UPLOAD_SONG
    UPLOAD_IMG='D:\downloads\\flask-music-streaming-master\\flask-music-streaming-master\static\\'
    app.config['UPLOAD_IMG'] = UPLOAD_IMG
    title = request.form["title"]
    artist = request.form["artist"]
    album =request.form["album"]
    uploadImage=request.files["image"]
    uploadSong=request.files["song"]
    record=(title,artist,album,"music/"+uploadSong.filename,"static\\"+uploadImage.filename)
    query="""INSERT INTO songs (title, artist,album,song,image) VALUES ( %s,%s, %s,%s,%s) """
    cursor=connection.cursor()
    cursor.execute(query,record)
    connection.commit()
    print("inserted")
    uploadImage.save(os.path.join(app.config['UPLOAD_IMG'], secure_filename(uploadImage.filename)))
    uploadSong.save(os.path.join(app.config['UPLOAD_SONG'], secure_filename(uploadSong.filename)))
    print("success")
    return render_template("success.html")

""" Removed functionality for better UX
@app.route('/getsongs',methods=["GET","POST"])
def getsongs():
    input = str(request.args.get("songname"));
    print(input)
    # get song from db
    data = return_dict()

    query = "select * from songs where title like \"%"+str(input)+"%\" or album like \"%"+str(input)+"%\" or artist like \"%"+str(input)+"%\" ; "
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in cursor.fetchall()]
    stream_entries = data
    print(data)
    return render_template('index.html', entries=stream_entries)
"""

#Route to delete a song permanently from Db
@app.route('/deletesong',methods=["GET","POST"])
def deletesong():
    dId=int(request.args.get("did"))
    #print(dId)
    query = "delete from songs where sid=" + str(dId) + ";"
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    query1 = " select * from songs;"
    result = cursor.execute(query1)
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in cursor.fetchall()]
    #print(data)
    return render_template("index.html", entries=data);



#Route to move to a particular song page
@app.route('/song',methods=["GET","POST"])
def song():
    songId=int(request.args.get("songId"))
    #get song from db
    data=return_dict()
    query="select * from songs where sid="+str(songId)+";"
    cursor=connection.cursor()
    cursor.execute(query)
    songDetails=cursor.fetchall();
    print(songDetails)
    return render_template("song.html",songDetails=songDetails);

#Running the app
if __name__ == "__main__":
    app.run("localhost",5000,debug=True);

    
