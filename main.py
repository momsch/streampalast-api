from flask import Flask, jsonify
from flask_cors import CORS
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app, origins=["https://streampalast.com", "https://www.streampalast.com", "https://streampalast.pages.dev", "*"])

TMDB_KEY = '62c6bf83f8d16425d45289653865ae0d'

def check(name, url):
    try:
        r = requests.head(url, timeout=3, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        return {"name": name, "url": url, "available": r.status_code < 500}
    except:
        return {"name": name, "url": url, "available": True}

def build_movie(tmdb_id):
    return [
        ("Server 1", f"https://vidsrc.me/embed/movie/{tmdb_id}"),
        ("Server 2", f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1"),
        ("Server 3", f"https://vidsrc.to/embed/movie/{tmdb_id}"),
        ("Server 4", f"https://autoembed.cc/movie/tmdb/{tmdb_id}"),
        ("Server 5", f"https://embed.su/embed/movie/{tmdb_id}"),
    ]

def build_tv(tmdb_id, s, e):
    return [
        ("Server 1", f"https://vidsrc.me/embed/tv/{tmdb_id}?season={s}&episode={e}"),
        ("Server 2", f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1&s={s}&e={e}"),
        ("Server 3", f"https://vidsrc.to/embed/tv/{tmdb_id}/{s}/{e}"),
        ("Server 4", f"https://autoembed.cc/tv/tmdb/{tmdb_id}-{s}-{e}"),
        ("Server 5", f"https://embed.su/embed/tv/{tmdb_id}/{s}/{e}"),
    ]

def test_all(sources):
    with ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(lambda x: check(x[0], x[1]), sources))
    results.sort(key=lambda x: not x['available'])
    return results

@app.route('/')
def home():
    return jsonify({"status": "StreamPalast API running", "endpoints": ["/stream/movie/<id>", "/stream/tv/<id>/<s>/<e>"]})

@app.route('/stream/movie/<int:tmdb_id>')
def movie(tmdb_id):
    return jsonify({"tmdb_id": tmdb_id, "sources": test_all(build_movie(tmdb_id))})

@app.route('/stream/tv/<int:tmdb_id>/<int:season>/<int:episode>')
def tv(tmdb_id, season, episode):
    return jsonify({"tmdb_id": tmdb_id, "season": season, "episode": episode, "sources": test_all(build_tv(tmdb_id, season, episode))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
