# YouTube Video Summarizer

This is a simple web app. It takes a YouTube URL and returns a summary of the video.

## What It Does

-   **Input:** A YouTube URL.
-   **Fetch:** The video transcript using the YouTube Transcript API.
-   **Summarize:** The transcript with OpenAI's API.
-   **Serve:** The backend with Flask and the frontend with Vue.js.

Both parts run in Docker containers managed by Docker Compose.

## How to Install

You need Docker and Docker Compose. Then, clone the repo and build the containers.

```bash
git clone https://github.com/Abhis33/Youtube-video-summarizer-AI.git
cd your-project-folder
docker-compose up --build
```

The backend runs on port 5000 and the Vue frontend on port 8080.

## How to Use

-   Open your browser and go to <http://localhost:8080>.
-   Type a YouTube URL in the box.
-   Press the button to get your summary.

License

This project is licensed under the MIT License.
