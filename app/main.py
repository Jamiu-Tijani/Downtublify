from flask import Flask,redirect,url_for,render_template,request
import youtube_dl
import pandas as pd
import numpy as np


app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process',methods = ['POST'])
def process():
    user_input= request.form["name"]
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
    'format': 'bestaudio/best',       
    'outtmpl': '%(id)s',        
    'noplaylist' : True,        
    'progress_hooks': [my_hook],  
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result= ydl.extract_info(url = user_input,download = False)
    i =0
    formats = []
    extension = []
    filesize = []
    link = []
    while i < len(result["formats"]):
        formats.append(result["formats"][i]['format_id'])
        extension.append(result["formats"][i]['ext'])
        filesize.append(result["formats"][i]['filesize'])
        link.append(result["formats"][i]['url'])
        i = i+1
    df = pd.DataFrame()
    df["format_id"] = formats
    df["extension"] = extension
    df["filesize"] = filesize
    df["links"] = link
    df["filesize"] = df["filesize"].apply(lambda x: str(np.trunc(x/1000000)) + "MB")
    ext = zip(extension,df["filesize"],link)
    return render_template('index.html',ext=ext)    
