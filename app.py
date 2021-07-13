import requests
from flask import Flask, render_template, Response,request
import sys
import mysql.connector
import os

from mysql.connector import connection

connection = mysql.connector.connect(host='localhost',
                                             database='music',
                                             user='root',
                                             password='root')
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
    general_Data = {
        'title': 'Music Player'}
    stream_entries = return_dict()

    return render_template('simple.html', entries=stream_entries, **general_Data)


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
    return render_template('simple.html', entries=stream_entries)

@app.route('/deletesong',methods=["GET","POST"])
def deletesong():
    dId=int(request.args.get("did"))
    print(dId)
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
    print(data)
    return render_template("simple.html", entries=data);




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

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    app.run(debug=True);

    
