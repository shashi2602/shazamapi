import random
import string
import requests
import base64
from pyDes import *

userAgents = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/17.17134",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/18.17763",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/19",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/45",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/46",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 OPR/47",
]


def generate_random_string(length: int):
  characters = characters = string.ascii_lowercase + string.digits
  random_string = ""
  for i in range(length):
    random_string += characters[random.randint(0, len(characters))]
  return random_string


def get_random_useragent():
  return userAgents[random.randint(0, len(userAgents) - 1)]


def get_headers():
  headers = {
    "Accept": "*/*",
    "Accept-Language": "en-us,en;q=0.5",
    "Sec-Fetch-Mode": "navigate",
    "Referer": "https://reelsaver.net/download-audio-instagram",
    "Origin": "https://reelsaver.net",
    "User-Agent": get_random_useragent(),
  }
  return headers


def get_reel_data(url: str):
  headers = get_headers()
  body = {"url": url, "ref": " download-audio-instagram", "via": "form"}
  res = requests.post("https://reelsaver.net/api/instagram",
                      data=body,
                      headers=headers)
  if res.status_code == 200:
    response = res.json()
    if response['success']:
      return response['data']['medias'][0]["src"]
  else:
    return ""


def convert_json(data):
  sections = {}
  for i in range(len(data['track']['sections'])):
    if data['track']['sections'][i]['type'] == "SONG":
      album = []
      if len(data['track']['sections'][i]['metadata']) != 0:
        for j in range(len(data['track']['sections'][i]['metadata'])):
          album.append(data['track']['sections'][i]['metadata'][j]['text'])
      else:
        album.append(data['track']['sections'][i]['metapages'][0]['caption'])
      sections['album'] = ' '.join(album)
    if data['track']['sections'][i]['type'] == "LYRICS":
      sections['lyrics'] = data['track']['sections'][i]['text']
    if data['track']['sections'][i]['type'] == "VIDEO":
      response = requests.get(data['track']['sections'][i]['youtubeurl'])
      if response.status_code == 200:
        yt_details = response.json()
        youtube = {
          "title": yt_details['caption'],
          "thumbnail": yt_details['image']['url'],
          "video_id": yt_details['actions'][0]['uri'].split("/")[-1][:11]
        }
        sections['youtube'] = youtube
  final_data = {
    "title":
    data['track']['title'],
    "subtitle":
    data['track']['subtitle'],
    "cover_art":
    data['track']['images']['coverart'],
    "meta_data":
    sections,
    'genere':
    data['track']['genres']['primary']
    if 'genres' in data['track'] else "Unknown",
    "message":
    "success"
  }
  return final_data

def get_song_from_spotify(song_name: str):
  return "coming sooon"

def decrypt_url(url):
    des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",
                     pad=None, padmode=PAD_PKCS5)
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp4")
    return dec_url

def get_song_form_saavan(song_name: str,genere:str):
  url:str = "https://www.jiosaavn.com/api.php?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query="
  song_url = "https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids="
  related_songs:dict = requests.get(url + song_name).json()["songs"]['data'][0:3] 
  list_songs = []
  for song in related_songs:
    media_url = requests.get(song_url+song['id']).json()[song['id']]['encrypted_media_url']
    song['media_url'] = decrypt_url(media_url)
    song['image'] = song['image'].replace("-50x50","-500x500")
    list_songs.append(song)
  return list_songs
