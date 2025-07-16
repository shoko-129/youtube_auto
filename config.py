# Configuration file for YouTube Automation

# Download settings
DOWNLOAD_CONFIG = {
    # Video quality format (SINGLE FILE ONLY - no separate audio/video)
    # 'best[ext=mp4]/best' - Downloads single MP4 file with video+audio combined
    # 'best' - Downloads single file in best available format
    'format': 'best[ext=mp4]/best',

    # Output format after merging
    'merge_format': 'mp4',
    
    # Number of retries for failed downloads
    'retries': 10,
    
    # Fragment retries for live streams
    'fragment_retries': 10,
    
    # Socket timeout in seconds
    'socket_timeout': 30,
    
    # Use external downloader (aria2c) if available
    'use_external_downloader': True,
    
    # Skip files that already exist
    'skip_existing': True,
    
    # Maximum file size in MB (0 = no limit)
    'max_filesize_mb': 0,
    
    # Minimum file size in MB (0 = no limit)
    'min_filesize_mb': 0,
}

# Format presets for different use cases (SINGLE FILE DOWNLOADS ONLY)
FORMAT_PRESETS = {
    # Single file downloads (no separate audio/video files)
    'simple': 'best[ext=mp4]/best',
    'quality_mp4': 'best[height<=1080][ext=mp4]/best[height<=1080]/best',
    'mobile_friendly': 'best[height<=720][ext=mp4]/best[height<=720]/best',

    # Audio only (single file)
    'audio_only': 'bestaudio[ext=m4a]/bestaudio/best',
}

# File and directory settings
FILE_CONFIG = {
    # Excel file containing URLs
    'excel_file': 'video_links.xlsx',
    
    # Column name in Excel file containing URLs
    'url_column': 'Link',
    
    # Downloads directory
    'downloads_dir': 'downloads',
    
    # Error log file
    'error_log': 'error_log.txt',
    
    # Downloaded files tracking
    'downloaded_log': 'downloaded_files.txt',
}

# Logging settings
LOGGING_CONFIG = {
    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'level': 'INFO',
    
    # Log format
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    
    # Also log to console
    'console_output': True,
}

# Upload settings (for upload_videos.py)
UPLOAD_CONFIG = {
    # Default privacy status: private, public, unlisted
    'privacy_status': 'public',
    
    # Default description
    'default_description': 'Uploaded automatically by YouTube Shorts Uploader',
    
    # Made for kids setting
    'made_for_kids': False,
    
    # Upload retry settings
    'max_retries': 3,
    'retry_delay': 5,  # seconds
    
    # Chunk size for uploads (in bytes)
    'chunk_size': 1024 * 1024,  # 1MB
}
