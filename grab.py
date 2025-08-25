import os
import json
from googleapiclient.discovery import build

def get_youtube_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    try:
        # Retrieve the uploads playlist ID of the channel
        channel_response = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()

        if 'items' not in channel_response or len(channel_response['items']) == 0:
            print("Channel not found.")
            return []

        playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Retrieve all videos from the uploads playlist
        videos = []
        next_page_token = None

        while True:
            playlist_items_response = youtube.playlistItems().list(
                playlistId=playlist_id,
                part='snippet',
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_items_response['items']]
            video_response = youtube.videos().list(
                id=','.join(video_ids),
                part='snippet,statistics,contentDetails'
            ).execute()

            for video in video_response['items']:
                if '#shorts' not in video['snippet']['description'].lower():
                    videos.append(video)

            next_page_token = playlist_items_response.get('nextPageToken')

            if not next_page_token:
                break

        return videos
    except Exception as e:
        print("An error occurred:", e)
        return []


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    API_KEY = ""
    CHANNEL_ID = ""

    videos = get_youtube_videos(API_KEY, CHANNEL_ID)

    # Save the videos data to a JSON file
    save_to_json(videos, 'youtube_videos.json')