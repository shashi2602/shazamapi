from api import Shazam
from flask import Flask,request
import urllib
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/',methods = ['GET'])
def get_song():
    song_link = request.args.get('url')
    mp3 = urllib.request.urlopen(song_link).read()
    shazam = Shazam(
        mp3,
    )
    recognize_generator = shazam.recognizeSong()
    return recognize_generator

@app.route('/status',methods = ['GET'])
def get_status():
    return "success",200

if __name__ == '__main__':
    app.run(debug=True)