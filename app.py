from flask import Flask, render_template, request
from spotify import get_recommendations, get_playlist_tracks

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('query')
    mood = request.form.get('mood')

    # 紀錄搜尋關鍵字（如果有輸入才紀錄）
    if user_input:
        with open("search_log.txt", "a", encoding="utf-8") as f:
            f.write(user_input.strip() + "\n")

    # 呼叫 Spotify API 取得推薦
    recommendations = get_recommendations(user_input, mood=mood)

    return render_template('results.html', songs=recommendations, query=user_input or mood)

@app.route('/top')
def top_searches():
    # Spotify 今日熱門榜單
    playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
    songs = get_playlist_tracks(playlist_id)
    return render_template("top.html", top_songs=songs)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
