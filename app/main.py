from flask import Flask,redirect,url_for,render_template,request
import youtube_dl




app=Flask(__name__)
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/process',methods = ['POST'])
def process():
    user_input= request.form["name"]
    youtube_dl.YoutubeDL().download([user_input])
    print()
    return render_template('Home.html')    
