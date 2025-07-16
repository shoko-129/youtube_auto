import os
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.oauth2.credentials

# Configuration
CLIENT_SECRETS_FILE = 'youtube_credentials.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
SHORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def get_authenticated_service():
    """Authenticate with YouTube API using OAuth2"""
    credentials = None
    token_file = 'token.json'

    if os.path.exists(token_file):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(token_file)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)
        
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    return build('youtube', 'v3', credentials=credentials)

def upload_short_with_retry(service, file_path, title):
    """Attempt upload with retry logic"""
    for attempt in range(MAX_RETRIES):
        try:
            print(f"\nUpload attempt {attempt + 1} of {MAX_RETRIES} for: {title}")
            
            body = {
                'snippet': {
                    'title': title,
                    'description': 'Uploaded automatically by YouTube Shorts Uploader',
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False,
                }
            }

            media = MediaFileUpload(
                file_path,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024
            )

            request = service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            last_progress = 0
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    if progress > last_progress:
                        print(f"Upload progress: {progress}%")
                        last_progress = progress

            video_id = response['id']
            return f"https://youtube.com/shorts/{video_id}"

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                raise

def main():
    print("\nYouTube Shorts Uploader\n" + "="*30)
    
    # Verify downloads directory exists
    if not os.path.exists(SHORTS_DIR):
        print(f"Error: Directory not found - {SHORTS_DIR}")
        return

    # Get authenticated service
    try:
        youtube = get_authenticated_service()
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return

    # Process files
    video_files = [f for f in os.listdir(SHORTS_DIR) if f.lower().endswith('.mp4')]
    
    if not video_files:
        print("No MP4 files found in downloads directory")
        return

    print(f"\nFound {len(video_files)} videos to upload:")
    for i, filename in enumerate(video_files, 1):
        print(f"{i}. {filename}")

    total = len(video_files)
    success = 0

    for filename in video_files:
        file_path = os.path.join(SHORTS_DIR, filename)
        title = os.path.splitext(filename)[0].replace('_', ' ')

        print(f"\nProcessing: {filename} ({title})")
        try:
            url = upload_short_with_retry(youtube, file_path, title)
            print(f"Success! View at: {url}")
            success += 1
        except Exception as e:
            print(f"Failed to upload {filename}: {str(e)}")

    print(f"\nUpload complete. Successfully uploaded {success} of {total} videos")

if __name__ == "__main__":
    main()