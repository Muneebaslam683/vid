from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def extract_youtube_tags(video_url):
    try:
        # Make a GET request to the video URL
        response = requests.get(video_url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all tags from meta tags with property 'og:video:tag'
        tags_meta_list = soup.find_all('meta', {'property': 'og:video:tag'})

        if tags_meta_list:
            # Loop through all meta tags and collect the tags
            all_tags = []
            for tags_meta in tags_meta_list:
                tags = tags_meta['content'].split(',')
                for tag in tags:
                    all_tags.append(tag.strip())
            return all_tags
        else:
            return ["No tags found for the given video."]

    except Exception as e:
        return [f"Error: {e}"]

@app.route('/extract_tags', methods=['GET'])
def api_extract_tags():
    video_url = request.args.get('video_url')

    if not video_url:
        return jsonify({"error": "Missing 'video_url' parameter"}), 400

    tags = extract_youtube_tags(video_url)
    return jsonify({"tags": tags})

if __name__ == '__main__':
    app.run(debug=True)
