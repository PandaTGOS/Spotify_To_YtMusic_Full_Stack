from ytmusicapi import YTMusic
from dotenv import load_dotenv
from requests import post, get
import json
import os
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv ("CLIENT_SECRET")


def get_token (): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf8")
    auth_base64 = str (base64. b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    
    if "access_token" in json_result: 
        token = json_result["access_token"]
        return token
    else:
        print(json_result)
        return None


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_playlist(link, token): 
    playlist_id = link.split("/")[4].split("?")[0] 
                             
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers = headers)
    json_result = json.loads(result.content)

    name = json_result["name"]
    tracks = json_result.get("tracks", {}).get("items", [])
    
    while json_result.get("tracks", {}).get("next"):
        next_url = json_result["tracks"]["next"]
        result = get(next_url, headers=headers)
        json_result = json.loads(result.content)
        tracks.extend(json_result.get("items", []))

    return name, tracks


def add_to_yt(song, yt, playlistId, socketio, i):
    query = song + " official audio" 
    search_results = yt.search(query, filter="songs", limit=1)
    if search_results:
        top_result = search_results[0]
        yt.add_playlist_items(playlistId, [top_result['videoId']])
        socketio.emit('update', {'message': f'{i}_Added: {song}'})
    else:
        socketio.emit('update', {'message': f'{i}_NOT FOUND: {song}'})


def Transfer(link, socketio):
    token = get_token()
    name, playlist = search_playlist(link, token)
    
    songs_list = [ str(song["track"]["name"] +" by "+ song["track"]["artists"][0]["name"]) for song in playlist]
    
    #yt
    yt = YTMusic('oauth.json')
    playlistId = yt.create_playlist(name, 'playlist '+name+' transferred from Spotify')

    socketio.emit('update', {'message': f'PLAYLIST: {name} : {len(songs_list)} Songs'})

    i=0
    for song in songs_list:
        i+=1
        try:
            add_to_yt(song, yt, playlistId, socketio, i)
        except Exception as e:
            print(e)
            continue
    
    socketio.emit('update', {'message': f' '})
    socketio.emit('update', {'message': f'Successfully transferred {name} !'})




#test_link
#https://open.spotify.com/playlist/5H1RoueEQHIrxaTaRJvmSc?si=3kvZFt9vQGWd7vr_NDNoXQ&pi=a-mYEsMLz2Qtme