from flask import Flask, redirect, url_for, render_template, request
import yt_dlp as youtube_dl  # Use yt-dlp instead of youtube_dl
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form["name"]

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s',
        'noplaylist': True,
        'progress_hooks': [my_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url=user_input, download=False)

    formats = []
    extensions = []
    filesizes = []
    links = []
    for format in result["formats"]:

        # Filter out formats that are not video files (e.g., storyboards, streams)
        if format.get('vcodec') != 'none' and format.get('acodec') != 'none':
            format_id = format.get('format_id')
            ext = format.get('ext')
            filesize = format.get('filesize', 0)  # Size might not always be available
            url = format.get('url')                
            formats.append(format_id)
            extensions.append(ext)
            filesizes.append(filesize)
            links.append(url)

    df = pd.DataFrame({
        "format_id": formats,
        "extension": extensions,
        "filesize": filesizes,
        "links": links
    })

    df["filesize"] = df["filesize"].apply(lambda x: str(np.trunc(x / 1000000)) + "MB" if x else "Unknown")
    print(df)
    ext = zip(extensions, df["filesize"], links)
    return render_template('index.html', ext=ext)

@app.route('/download', methods=['POST'])
def download():
    print(type(request.form.get('service')))
    return render_template('index.html')
