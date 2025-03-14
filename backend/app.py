from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from urllib.parse import urlparse, parse_qs
import os

app = Flask(__name__)

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Added API key

# Apply CORS to all routes for better security control
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

def extract_video_id(youtube_url):
    if not youtube_url:
        return None

    parsed_url = urlparse(youtube_url)
    hostname = parsed_url.hostname.lower() if parsed_url.hostname else ""

    if hostname in ["youtu.be"]:
        return parsed_url.path[1:]
    elif hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        elif parsed_url.path.startswith("/embed/"):
            return parsed_url.path.split("/")[2]
        elif parsed_url.path.startswith("/v/"):
            return parsed_url.path.split("/")[2]
    return None

def summarize_text_with_openai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that summarizes text."},
                {"role": "user", "content": f"Summarize this text and extract key points: {text}"}
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        # Log the error instead of raising it
        print(f"OpenAI API error: {str(e)}")
        return f"Error generating summary: {str(e)}"

@app.route('/summarize', methods=['POST'])
def summarize_video():
    print("Init run")
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    youtube_url = data.get("url")
    print(f"Received URL: {youtube_url}")

    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    video_id = extract_video_id(youtube_url)
    print(f"Extracted video ID: {video_id}")

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item['text'] for item in transcript_list])
    except Exception as e:
        print(f"Transcript error: {str(e)}")
        return jsonify({"error": f"Error fetching transcript: {str(e)}"}), 500

    print(f"Transcript length: {len(transcript)} characters")

    try:
        summary_text = summarize_text_with_openai(transcript)
        if summary_text.startswith("Error generating summary"):
            return jsonify({"error": summary_text}), 500
    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return jsonify({"error": f"Error during summarization: {str(e)}"}), 500

    return jsonify({"summary": summary_text})

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {str(e)}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':  # Fixed syntax error here
    app.run(host='0.0.0.0', port=5000)
