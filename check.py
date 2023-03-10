from api import Shazam
from flask import Flask,request,jsonify
import urllib

app=Flask(__name__)

@app.route('/',methods = ['GET'])
def get_song():
    song_link = request.args.get('url')
    mp3 = urllib.request.urlopen(song_link).read()
    shazam = Shazam(
        mp3,
    )
    recognize_generator = shazam.recognizeSong()
    return recognize_generator


if __name__ == '__main__':
    app.run(debug=True)