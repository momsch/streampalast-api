from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

TMDB_KEY = '62c6bf83f8d16425d45289653865ae0d'

def get_imdb_id(tmdb_id, media_type='movie'):
    try:
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}/external_ids?api_key={TMDB_KEY}"
        r = requests.get(url, timeout=5)
        return r.json().get('imdb_id', '')
    except:
        return ''

@app.route('/')
def home():
    return jsonify({"status": "StreamPalast API running"})

@app.route('/stream/movie/<int:tmdb_id>')
def stream_movie(tmdb_id):
    imdb_id = get_imdb_id(tmdb_id, 'movie')
    sources = []
    if imdb_id:
        sources.append({"name":"Server 1","url":f"https://vidsrc.me/embed/movie?imdb={imdb_id}","quality":"HD"})
        sources.append({"name":"Server 2","url":f"https://autoembed.cc/movie/imdb/{imdb_id}","quality":"HD"})
        sources.append({"name":"Server 3","url":f"https://www.2embed.cc/embed/{imdb_id}","quality":"HD"})
    sources.append({"name":"Server 4","url":f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1","quality":"HD"})
    return jsonify({"tmdb_id":tmdb_id,"imdb_id":imdb_id,"sources":sources})

@app.route('/stream/tv/<int:tmdb_id>/<int:season>/<int:episode>')
def stream_tv(tmdb_id, season, episode):
    imdb_id = get_imdb_id(tmdb_id, 'tv')
    sources = []
    if imdb_id:
        sources.append({"name":"Server 1","url":f"https://vidsrc.me/embed/tv?imdb={imdb_id}&season={season}&episode={episode}","quality":"HD"})
        sources.append({"name":"Server 2","url":f"https://autoembed.cc/tv/imdb/{imdb_id}-{season}-{episode}","quality":"HD"})
        sources.append({"name":"Server 3","url":f"https://www.2embed.cc/embedtv/{imdb_id}&s={season}&e={episode}","quality":"HD"})
    sources.append({"name":"Server 4","url":f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1&s={season}&e={episode}","quality":"HD"})
    return jsonify({"tmdb_id":tmdb_id,"imdb_id":imdb_id,"season":season,"episode":episode,"sources":sources})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
