from api import Shazam
from flask import Flask,request,jsonify
import requests as rs
from flask_cors import CORS
from datetime import datetime
from utils import get_reel_data
import os
from utils import generate_random_string,get_reel_data,convert_json,get_song_form_saavan
from spotify import spotify_search

app=Flask(__name__)
CORS(app)

@app.route('/findSong', methods=['GET', 'POST'])
# @limiter.limit("5/minute")
def get_song():
  if request.method == "POST":
    song_file = request.files.get("file")
    temp_file_name = generate_random_string(6) + ".wav"
    song_file.save(temp_file_name)
    start = datetime.now()
    mp3 = open(temp_file_name, 'rb').read()
    if os.path.exists(temp_file_name):
      os.remove(temp_file_name)
    shazam_post = Shazam(mp3, )
    rg = shazam_post.recognizeSong()
    try:
      if rg != None:
        final_data = convert_json(rg)
        final_data['time_taken'] = str(datetime.now() - start) + "sec"
        return final_data
      else:
        return jsonify({'message': "Song NotFound"})
    except:
      return jsonify({'message': 'exception occured'})

  if request.method == 'GET':
    url:str = request.args.get("url")
    if "instagram.com" in url:
      insta_audio_url = get_reel_data(url)
      if len(insta_audio_url)!=0:
        audio_bytes = rs.get(insta_audio_url).content
        shazam_get = Shazam(audio_bytes, )
        rec_data = shazam_get.recognizeSong()
        try:
          if rec_data!=None:
            final_data = convert_json(rec_data)
            saavan_data = get_song_form_saavan(final_data['title'],final_data['genere'])
            final_data ["related_songs"] = saavan_data
            return final_data
          else:
            return jsonify({'message': "Song NotFound"})
        except:
          return jsonify({'message': 'exception occured while fetching instagram data'})
      else:
        return jsonify({'message': 'error while getting audio from instagram link'})
    else:
      return jsonify({'message': 'submit an valid instagram link'})
  else:
    return jsonify({'message': "Only POST and GET requests are accepted"})

@app.route('/',methods = ['GET'])
def get_status():
    spty = spotify_search("Kilimanjaro")
    return jsonify(spty)

if __name__ == '__main__':
    app.run(debug=True)