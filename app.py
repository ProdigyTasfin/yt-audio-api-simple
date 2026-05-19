import yt_dlp
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/audio/<video_id>')
def get_audio_url(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio',
        'extract_flat': True,           # Do not fetch full video info – saves memory
        'skip_download': True,
        'ignoreerrors': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # The 'formats' list may be missing when extract_flat=True,
            # so fallback to direct 'url' if it's a direct audio format
            if 'url' in info and info.get('acodec') != 'none':
                return jsonify({'url': info['url'], 'title': info.get('title', '')})
            # Otherwise try to find a format that is audio-only
            formats = info.get('formats', [])
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    return jsonify({'url': f['url'], 'title': info.get('title', '')})
            return jsonify({'error': 'No audio stream found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
