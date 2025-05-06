from flask import Flask, render_template, request
import pandas as pd
from main import get_recommendations, get_playlist_tracks

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# 推薦頁
@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('query')
    emotion = request.form.get('emotion')
    genre = request.form.get('genre')
    exclude = request.form.get('exclude', '')  # 保持防重複機制（可選）

    exclude_list = exclude.split(',') if exclude else []

    if genre and emotion:
        if genre == "Folk":
            df = pd.read_csv('Genre/Folk.csv')
        elif genre == "Metal":
            df = pd.read_csv('Genre/Metal.csv')
        elif genre == "Rap":
            df = pd.read_csv('Genre/Rap.csv')
        elif genre == "Rock":
            df = pd.read_csv('Genre/Rock.csv')
        elif genre == "Pop":
            df = pd.read_csv('Genre/Pop.csv')
        elif genre == "Jazz":
            df = pd.read_csv('Genre/Jazz.csv')
        elif genre == "Electronic":
            df = pd.read_csv('Genre/Electronic.csv')
        elif genre == "Hip_Hop":
            df = pd.read_csv('Genre/Hip_Hop.csv')
        elif genre == "Classical":
            df = pd.read_csv('Genre/Classical.csv')
        elif genre == "Soundtrack":
            df = pd.read_csv('Genre/Soundtrack.csv')
        
        # 在 Genre 過濾後的 df 中，再篩選符合 Emotion 的
        df_filtered = df[df['emotion'] == emotion]

        # 如果篩到沒有歌，可以補救，例如隨便給3首 genre 內的歌
        if df_filtered.empty:
            return f"此篩選條件無結果"
        else:
            songs = df_filtered[['Artist', 'song', 'Album', 'ReleaseDate']].sample(min(3, len(df_filtered))).to_dict(orient='records')

        return render_template('genre_emotion_result.html', songs=songs, genre=genre, emotion=emotion)

    elif genre:
        # 只有選 genre
        if genre == "Folk":
            df = pd.read_csv('Genre/Folk.csv')
        elif genre == "Metal":
            df = pd.read_csv('Genre/Metal.csv')
        elif genre == "Rap":
            df = pd.read_csv('Genre/Rap.csv')
        elif genre == "Rock":
            df = pd.read_csv('Genre/Rock.csv')
        elif genre == "Pop":
            df = pd.read_csv('Genre/Pop.csv')
        elif genre == "Jazz":
            df = pd.read_csv('Genre/Jazz.csv')
        elif genre == "Electronic":
            df = pd.read_csv('Genre/Electronic.csv')
        elif genre == "Hip_Hop":
            df = pd.read_csv('Genre/Hip_Hop.csv')
        elif genre == "Classical":
            df = pd.read_csv('Genre/Classical.csv')
        elif genre == "Soundtrack":
            df = pd.read_csv('Genre/Soundtrack.csv')

        songs = df[['Artist', 'song', 'Album', 'ReleaseDate']].sample(3).to_dict(orient='records')
        return render_template('genre_result.html', songs=songs, genre=genre)

    elif emotion:
        if emotion == "anger":
            df = pd.read_csv('Emotion/anger.csv')
        elif emotion == "joy":
            df = pd.read_csv('Emotion/joy.csv')
        elif emotion == "love":
            df = pd.read_csv('Emotion/love.csv')
        elif emotion == "saddness":
            df = pd.read_csv('Emotion/saddness.csv')
        elif emotion == "lofi":
            df = pd.read_csv('Emotion/lofi.csv')
        elif emotion == "chillwave":
            df = pd.read_csv('Emotion/chillwave.csv')

        songs = df[['Artist', 'song', 'Album', 'ReleaseDate']].sample(3).to_dict(orient='records')
        return render_template('emotion_result.html', songs=songs, emotion=emotion)

    else:
        recommendations = get_recommendations(user_input, emotion=emotion, genre=genre, exclude=exclude_list)
    
    # 限制推薦數量為 3 首
    recommendations = recommendations[:3]  # 只保留前三首歌曲

    # 紀錄搜尋（如果有輸入）
    if user_input:
        with open("search_log.txt", "a", encoding="utf-8") as f:
            f.write(user_input.strip() + "\n")

    # 傳推薦結果
    current_recommendations = [song['title'] for song in recommendations]
    all_recommendations = exclude_list + current_recommendations

    return render_template('results.html',
                            songs=recommendations,
                            query=user_input or emotion or genre,
                            previous_recommendations=all_recommendations)

@app.route('/recommend_again', methods=['POST'])
def recommend_again():
    genre = request.form.get('genre')
    emotion = request.form.get('emotion')

    if genre and emotion:
        df = pd.read_csv(f'Genre/{genre}.csv')
        df = pd.read_csv(f'Emotion/{emotion}.csv')
    elif genre:
        df = pd.read_csv(f'Genre/{genre}.csv')
    else:
        df = pd.read_csv(f'Emotion/{emotion}.csv')

    # 隨機取三首
    songs = df[['Artist', 'song', 'Album', 'ReleaseDate']].drop_duplicates(subset='song').sample(min(3, len(df))).to_dict(orient='records')

    # 渲染原本的推薦結果頁
    if genre and emotion:
        return render_template('genre_emotion_result.html', songs=songs, genre=genre)
    elif genre:
        return render_template('genre_result.html', songs=songs, genre=genre)
    else:
        return render_template('emotion_result.html', songs=songs, emotion=emotion)

@app.route('/top') #大致無誤，yt搜尋看看能否更進步
def top_searches():
    # 讀取數據集
    df = pd.read_csv('universal_top_spotify_songs.csv')
    # 選擇需要顯示的列
    songs = df[['name', 'artists','daily_rank']].head(50).to_dict(orient='records')
    # 渲染 HTML 模板，傳遞數據
    return render_template('top.html', songs=songs)

@app.route('/random', methods=['GET', 'POST'])
def ran_searches():
    # 讀取數據集
    df = pd.read_csv('spotify_dataset.csv')
    # 選擇需要顯示的列
    songs = df[['Artist', 'song', 'Album', 'ReleaseDate']].sample(3).to_dict(orient='records')
    # 渲染 HTML 模板，傳遞數據
    return render_template('random.html', songs=songs)

if __name__ == '__main__':
    app.run(debug=True)
