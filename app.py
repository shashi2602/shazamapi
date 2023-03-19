from api import Shazam
from flask import Flask,request,jsonify
import urllib
import requests as rs
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/findSong',methods = ['GET'])
def get_song():
    song_link = request.args.get('url')
    mp3 = urllib.request.urlopen(song_link).read()
    shazam = Shazam(
        mp3,
    )
    rg = shazam.recognizeSong()
    if rg!=None:
      sections = {}
      for i in range(len(rg['track']['sections'])):
        if rg['track']['sections'][i]['type']=="SONG":
          sections['album']=rg['track']['sections'][i]['metadata'][0]['text']
        if rg['track']['sections'][i]['type']=="LYRICS":
          sections['lyrics']= rg['track']['sections'][i]['text']
        if rg['track']['sections'][i]['type']=="VIDEO":
          response=rs.get(rg['track']['sections'][i]['youtubeurl'])
          if response.status_code==200:
            yt_details=response.json()
            youtube={
              "title":yt_details['caption'],
              "thumbnail":yt_details['image']['url'],
              "video_url":yt_details['actions'][0]['uri']
            }
            sections['youtube']=youtube
          
      final_data={
        "title":rg['track']['title'],
        "subtitle":rg['track']['subtitle'],
        "cover_art":rg['track']['images']['coverart'],
        "meta_data":sections,
        'genere':rg['track']['genres']['primary']
      }
      return final_data
    else:
       return jsonify({'message':"NotFound"})

@app.route('/',methods = ['GET'])
def get_status():
    return "success",200

if __name__ == '__main__':
    app.run(debug=True)