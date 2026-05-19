import yt_dlp
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/audio/<video_id>')
def get_audio_url(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio',
            'extract_flat': 'in_playlist',  # Tells yt-dlp to not resolve all formats
            'skip_download': True,           # Avoids downloading any data
            'ignoreerrors': True,            # Prevents parsing errors from causing memory spikes
            'max_entries': 1,                # Limits entries for playlists
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Find the best audio format (as a fallback, you can still use this)
            formats = info.get('formats', [])
            audio_url = None
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    audio_url = f.get('url')
                    break
            if audio_url:
                return jsonify({'url': audio_url, 'title': info.get('title', '')})
            else:
                return jsonify({'error': 'No audio stream found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
