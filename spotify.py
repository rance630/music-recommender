import requests
import base64

CLIENT_ID = "d46eb57fc8b64af89e739269acc8f28a"
CLIENT_SECRET = "9e6351eb9fec4cf5ad1011037c575241"

def get_access_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    res = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if res.status_code != 200:
        print("[Error] 無法取得 access token:", res.text)
        return None

    token = res.json().get("access_token")
    return token

def get_recommendations(query, mood=None, limit=6):
    token = get_access_token()
    if not token:
        return []

    # 如果沒打關鍵字但有選心情
    if mood and not query:
        mood_keywords = {
            'relax': 'lofi chill',
            'energetic': 'workout hype',
            'reflective': 'acoustic sad',
            'happy': 'summer party',
            'sleepy': 'ambient sleep'
        }
        query = mood_keywords.get(mood, 'chill')

    headers = {"Authorization": f"Bearer {token}"}
    try:
        params = {"q": query, "type": "track", "limit": limit}
        res = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

        if res.status_code != 200:
            print("[Error] Spotify API 回傳錯誤:", res.text)
            return []

        tracks = res.json().get("tracks", {}).get("items", [])
        results = []
        for item in tracks:
            title = item.get("name", "Unknown")
            artist = item.get("artists", [{}])[0].get("name", "Unknown")
            album = item.get("album", {})
            images = album.get("images", [])
            cover_url = images[0]["url"] if images else ""

            results.append({
                "title": title,
                "artist": artist,
                "cover_url": cover_url,
                "preview_url": item.get("preview_url", ""),
                "youtube_embed_url": f"https://www.youtube.com/results?search_query={title}+{artist}"
            })
        return results

    except Exception as e:
        print("[Exception] 發生例外錯誤：", e)
        return []

def get_playlist_tracks(playlist_id):
    token = get_access_token()
    if not token:
        return []

    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    res = requests.get(url, headers=headers)
    print("🔍 Spotify Playlist API 狀態碼：", res.status_code)
    if res.status_code != 200:
        print("[Error] 無法取得歌單資料:", res.text)
        return []

    items = res.json().get("items", [])
    print(f"✅ 取得 {len(items)} 首歌曲")

    results = []
    for item in items:
        track = item.get("track", {})
        title = track.get("name", "Unknown")
        artist = track.get("artists", [{}])[0].get("name", "Unknown")
        album = track.get("album", {})
        images = album.get("images", [])
        cover_url = images[0]["url"] if images else ""

        results.append({
            "title": title,
            "artist": artist,
            "cover_url": cover_url,
            "preview_url": track.get("preview_url", ""),
            "youtube_embed_url": f"https://www.youtube.com/results?search_query={title}+{artist}"
        })
    return results
