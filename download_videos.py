import pandas as pd
import subprocess
import os
import shutil
import sys
from pathvalidate import sanitize_filename
import logging
from datetime import datetime
try:
    from config import DOWNLOAD_CONFIG, FILE_CONFIG, LOGGING_CONFIG
except ImportError:
    # Default configuration if config.py is not found
    DOWNLOAD_CONFIG = {
        'format': 'bestvideo+bestaudio/best',
        'merge_format': 'mp4',
        'retries': 10,
        'fragment_retries': 10,
        'socket_timeout': 30,
        'use_external_downloader': True,
        'skip_existing': True,
        'max_filesize_mb': 0,
        'min_filesize_mb': 0,
    }
    FILE_CONFIG = {
        'excel_file': 'video_links.xlsx',
        'url_column': 'Link',
        'downloads_dir': 'downloads',
        'error_log': 'error_log.txt',
        'downloaded_log': 'downloaded_files.txt',
    }
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'console_output': True,
    }

# Set up directories and logging
DOWNLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_CONFIG['downloads_dir'])
ERROR_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_CONFIG['error_log'])
DOWNLOADED_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILE_CONFIG['downloaded_log'])

# Ensure downloads directory exists
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Configure logging
log_level = getattr(logging, LOGGING_CONFIG['level'].upper())
logging.basicConfig(
    filename=ERROR_LOG,
    level=log_level,
    format=LOGGING_CONFIG['format']
)

# Add console handler if configured
if LOGGING_CONFIG['console_output']:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter(LOGGING_CONFIG['format'])
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

def find_ytdlp():
    """Find yt-dlp executable in system PATH or common locations"""
    # Try to find yt-dlp in PATH first
    ytdlp_path = shutil.which('yt-dlp')
    if ytdlp_path:
        return ytdlp_path

    # Try common installation locations
    common_paths = []

    if sys.platform == "win32":
        # Windows common paths
        common_paths = [
            os.path.expanduser(r'~\AppData\Roaming\Python\Python*\Scripts\yt-dlp.exe'),
            os.path.expanduser(r'~\AppData\Local\Programs\Python\Python*\Scripts\yt-dlp.exe'),
            r'C:\Python*\Scripts\yt-dlp.exe',
        ]
    else:
        # Unix-like systems (Linux, macOS)
        common_paths = [
            '/usr/local/bin/yt-dlp',
            '/usr/bin/yt-dlp',
            os.path.expanduser('~/.local/bin/yt-dlp'),
        ]

    # Check each path
    for path_pattern in common_paths:
        if '*' in path_pattern:
            # Handle wildcard paths
            import glob
            matches = glob.glob(path_pattern)
            if matches:
                return matches[0]
        elif os.path.isfile(path_pattern):
            return path_pattern

    # If not found, assume it's in PATH and let subprocess handle the error
    return 'yt-dlp'

def sanitize_title(title):
    """Sanitize video title to make it suitable for filename"""
    return sanitize_filename(title).replace(' ', '_')

def load_downloaded_urls():
    """Load previously downloaded URLs from log file"""
    downloaded_urls = set()
    if os.path.exists(DOWNLOADED_LOG):
        try:
            with open(DOWNLOADED_LOG, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        downloaded_urls.add(line.strip())
        except Exception as e:
            logging.warning(f"Could not read downloaded log: {e}")
    return downloaded_urls

def save_downloaded_url(url):
    """Save successfully downloaded URL to log file"""
    try:
        with open(DOWNLOADED_LOG, 'a', encoding='utf-8') as f:
            f.write(f"{url}\n")
    except Exception as e:
        logging.warning(f"Could not save to downloaded log: {e}")

def is_valid_youtube_url(url):
    """Check if URL is a valid YouTube URL"""
    if not isinstance(url, str):
        return False

    youtube_patterns = [
        'youtube.com/watch',
        'youtube.com/shorts',
        'youtu.be/',
        'm.youtube.com/watch',
        'www.youtube.com/watch',
        'www.youtube.com/shorts'
    ]

    return any(pattern in url.lower() for pattern in youtube_patterns) and url.startswith(('http://', 'https://'))

def get_input_method():
    """Ask user to choose input method"""
    print("\n" + "="*50)
    print("📥 CHOOSE INPUT METHOD")
    print("="*50)
    print("1. 📄 Read URLs from Excel file (video_links.xlsx)")
    print("2. ⌨️  Enter URLs manually in terminal")
    print("="*50)

    while True:
        choice = input("Choose option (1 or 2): ").strip()
        if choice == '1':
            return 'excel'
        elif choice == '2':
            return 'terminal'
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

def get_urls_from_terminal():
    """Get YouTube URLs from terminal input"""
    print("\n" + "="*50)
    print("⌨️  MANUAL URL INPUT")
    print("="*50)

    while True:
        try:
            num_videos = int(input("How many videos do you want to download? "))
            if num_videos > 0:
                break
            else:
                print("❌ Please enter a number greater than 0.")
        except ValueError:
            print("❌ Please enter a valid number.")

    urls = []
    print(f"\n📝 Please enter {num_videos} YouTube URLs:")
    print("💡 Tip: You can paste URLs directly from your browser")
    print("-" * 50)

    for i in range(num_videos):
        while True:
            url = input(f"URL {i+1}/{num_videos}: ").strip()

            if not url:
                print("❌ URL cannot be empty. Please try again.")
                continue

            if is_valid_youtube_url(url):
                urls.append(url)
                print(f"✅ URL {i+1} added successfully")
                break
            else:
                print("❌ Invalid YouTube URL. Please enter a valid YouTube URL.")
                print("   Examples: https://youtube.com/watch?v=... or https://youtube.com/shorts/...")

    # Ask if user wants to save URLs to Excel for future use
    print("\n" + "-" * 50)
    save_choice = input("💾 Save these URLs to Excel file for future use? (y/n): ").strip().lower()

    if save_choice in ['y', 'yes']:
        try:
            import pandas as pd
            df = pd.DataFrame({'Link': urls})
            excel_file = FILE_CONFIG['excel_file']
            df.to_excel(excel_file, index=False)
            print(f"✅ URLs saved to {excel_file}")
        except Exception as e:
            print(f"⚠️  Could not save to Excel: {e}")

    return urls

def download_video(url, downloaded_urls):
    """Download YouTube video using yt-dlp"""
    ytdlp_path = find_ytdlp()

    # Check if URL was already downloaded
    if DOWNLOAD_CONFIG['skip_existing'] and url in downloaded_urls:
        logging.info(f"URL already downloaded previously, skipping: {url}")
        return True, "Previously downloaded (skipped)"

    try:
        # Get video title
        title_cmd = [
            ytdlp_path,
            '--get-title',
            '--no-warnings',
            url
        ]
        result = subprocess.run(title_cmd, capture_output=True, text=True, check=True)
        title = result.stdout.strip()

        # Sanitize title for filename
        safe_title = sanitize_title(title)
        output_path = os.path.join(DOWNLOADS_DIR, f"{safe_title}.%(ext)s")

        # Check if file already exists
        if DOWNLOAD_CONFIG['skip_existing']:
            potential_files = [
                os.path.join(DOWNLOADS_DIR, f"{safe_title}.{DOWNLOAD_CONFIG['merge_format']}"),
                os.path.join(DOWNLOADS_DIR, f"{safe_title}.webm"),
                os.path.join(DOWNLOADS_DIR, f"{safe_title}.mkv")
            ]

            for existing_file in potential_files:
                if os.path.exists(existing_file):
                    logging.info(f"File already exists, skipping: {existing_file}")
                    save_downloaded_url(url)  # Track this URL as downloaded
                    return True, f"{title} (file already exists)"

        # Build download command (single file download only)
        download_cmd = [
            ytdlp_path,
            '-f', DOWNLOAD_CONFIG['format'],  # Single file format only
            '--retries', str(DOWNLOAD_CONFIG['retries']),
            '--fragment-retries', str(DOWNLOAD_CONFIG['fragment_retries']),
            '--socket-timeout', str(DOWNLOAD_CONFIG['socket_timeout']),
            '-o', output_path,
            '--no-warnings',
            url
        ]

        # Add file size limits if configured
        if DOWNLOAD_CONFIG['max_filesize_mb'] > 0:
            download_cmd.extend(['--max-filesize', f"{DOWNLOAD_CONFIG['max_filesize_mb']}M"])

        if DOWNLOAD_CONFIG['min_filesize_mb'] > 0:
            download_cmd.extend(['--min-filesize', f"{DOWNLOAD_CONFIG['min_filesize_mb']}M"])

        # Add external downloader if configured and available
        if DOWNLOAD_CONFIG['use_external_downloader'] and shutil.which('aria2c'):
            download_cmd.extend(['--external-downloader', 'aria2c'])

        subprocess.run(download_cmd, check=True)
        logging.info(f"Successfully downloaded: {title}")

        # Save URL to downloaded log
        save_downloaded_url(url)

        return True, title
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to download {url}: {str(e)}"
        logging.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error with {url}: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

def process_urls_from_excel():
    """Process URLs from Excel file"""
    excel_file = FILE_CONFIG['excel_file']
    url_column = FILE_CONFIG['url_column']

    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"❌ Error: {excel_file} file not found in current directory")
        return None
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return None

    if url_column not in df.columns:
        print(f"❌ Error: Excel file must contain a '{url_column}' column")
        print(f"   Found columns: {list(df.columns)}")
        return None

    # Extract URLs from DataFrame
    urls = []
    for _, row in df.iterrows():
        url = row[url_column]
        if pd.notna(url) and isinstance(url, str) and url.startswith(('http://', 'https://')):
            urls.append(url)

    return urls

def main():
    start_time = datetime.now()
    print("🚀 YouTube Video Downloader")
    print("=" * 50)
    print(f"📁 Downloads will be saved to: {DOWNLOADS_DIR}")
    print(f"📝 Logs will be saved to: {ERROR_LOG}")

    # Check if yt-dlp is available
    ytdlp_path = find_ytdlp()
    try:
        subprocess.run([ytdlp_path, '--version'], capture_output=True, check=True)
        print(f"✅ Found yt-dlp at: {ytdlp_path}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: yt-dlp not found. Please install it using:")
        print("   pip install yt-dlp")
        print("   or visit: https://github.com/yt-dlp/yt-dlp")
        return

    # Load previously downloaded URLs
    downloaded_urls = load_downloaded_urls()
    if downloaded_urls:
        print(f"📋 Found {len(downloaded_urls)} previously downloaded URLs")

    # Get input method choice
    input_method = get_input_method()

    # Get URLs based on chosen method
    if input_method == 'excel':
        print("\n📄 Reading URLs from Excel file...")
        urls = process_urls_from_excel()
        if urls is None:
            return
    else:  # terminal input
        urls = get_urls_from_terminal()

    if not urls:
        print("❌ No valid URLs found to process")
        return

    total = len(urls)
    success_count = 0
    fail_count = 0
    skipped_count = 0

    print(f"\n📊 Processing {total} URLs...")
    print("=" * 50)

    for index, url in enumerate(urls):
        print(f"\n[{index + 1}/{total}] Processing: {url}")

        if is_valid_youtube_url(url):
            success, result = download_video(url, downloaded_urls)

            if success:
                if any(skip_text in result for skip_text in ["already downloaded", "already exists", "skipped"]):
                    print(f"⏭️  Skipped: {result}")
                    skipped_count += 1
                else:
                    print(f"✅ Successfully downloaded: {result}")
                    success_count += 1
            else:
                print(f"❌ Failed to download: {result}")
                fail_count += 1
        else:
            print(f"⚠️  Skipping invalid URL: {url}")
            fail_count += 1

    end_time = datetime.now()
    duration = end_time - start_time

    print("\n" + "="*60)
    print("📈 DOWNLOAD SUMMARY")
    print("="*60)
    print(f"📊 Total URLs processed: {total}")
    print(f"✅ Successfully downloaded: {success_count}")
    print(f"⏭️  Already existed (skipped): {skipped_count}")
    print(f"❌ Failed downloads: {fail_count}")
    print(f"⏱️  Time taken: {duration}")
    print(f"📁 Downloads saved to: {DOWNLOADS_DIR}")
    print(f"📝 Error log: {ERROR_LOG}")

    if success_count > 0:
        print(f"\n🎉 Successfully downloaded {success_count} videos!")
        print("💡 You can now run 'python3 upload_videos.py' to upload them to YouTube")
    else:
        print("\n⚠️  No videos were downloaded")

    print("="*60)

if __name__ == "__main__":
    main()