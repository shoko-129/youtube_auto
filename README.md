# YouTube Video Downloader & Uploader
**Version 1.0.0**

Hey there! 👋

Tired of manually downloading YouTube videos one by one? This tool makes it super easy to download multiple YouTube videos at once and even upload them back to YouTube if you want.

## What does this do?

Think of this as your personal YouTube assistant that can:

- **Download videos in bulk** - Give it a list of YouTube links and it downloads them all
- **Two ways to add links** - Either create an Excel file with your links OR just type them directly when you run the script
- **Smart enough to skip duplicates** - Won't waste time downloading the same video twice
- **Works on any computer** - Windows, Mac, Linux - doesn't matter what you use
- **Shows you what's happening** - Nice progress bars and emojis so you know it's working
- **Upload to YouTube** - Can take your downloaded videos and upload them to your YouTube channel

## Why would I use this?

- You're a content creator who needs to download videos for editing
- You want to backup your favorite videos
- You need to download multiple videos for a project
- You want to re-upload videos to your channel (with proper permissions, of course!)

## How to install this?

Don't worry, it's easier than you think! Just follow the steps for your computer:

### 🪟 **Windows Users**

1. **Download Python** (if you don't have it)
   - Go to [python.org](https://python.org) and download Python 3.8 or newer
   - During installation, check "Add Python to PATH"

2. **Download this project**
   ```cmd
   git clone https://github.com/Shiva-129/youtube_automation.git
   cd youtube_automation
   ```

3. **Install the required stuff**
   ```cmd
   python install_dependencies.py
   ```

   Or manually:
   ```cmd
   pip install pandas pathvalidate yt-dlp openpyxl
   ```

### 🍎 **Mac Users**

1. **Install Homebrew** (if you don't have it)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**
   ```bash
   brew install python
   ```

3. **Download this project**
   ```bash
   git clone https://github.com/Shiva-129/youtube_automation.git
   cd youtube_automation
   ```

4. **Install the required stuff**
   ```bash
   python3 install_dependencies.py
   ```

   Or manually:
   ```bash
   pip3 install pandas pathvalidate yt-dlp openpyxl
   ```

### 🐧 **Linux Users**

1. **Install Python** (probably already installed)
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

2. **Download this project**
   ```bash
   git clone https://github.com/Shiva-129/youtube_automation.git
   cd youtube_automation
   ```

3. **Install the required stuff**
   ```bash
   python3 install_dependencies.py
   ```

   Or manually:
   ```bash
   pip3 install pandas pathvalidate yt-dlp openpyxl
   ```

## How to use this?

Super simple! You have two ways to give it your YouTube links:

### 🎯 **Method 1: Just run it and type your links**

This is the easiest way:

1. **Run the script**
   ```bash
   # Windows
   python download_videos.py

   # Mac/Linux
   python3 download_videos.py
   ```

2. **Choose option 2** when it asks
3. **Tell it how many videos** you want to download
4. **Paste your YouTube links** one by one
5. **Sit back and watch** it download everything!

### 📄 **Method 2: Use an Excel file**

If you have lots of links or want to save them for later:

1. **Create an Excel file** called `video_links.xlsx`
2. **Add a column called "Link"** and put your YouTube URLs there
3. **Run the script** and **choose option 1**

### 🎬 **What you'll see when you run it:**

```
📥 CHOOSE INPUT METHOD
==================================================
1. 📄 Read URLs from Excel file (video_links.xlsx)
2. ⌨️  Enter URLs manually in terminal
==================================================
Choose option (1 or 2): 2

How many videos do you want to download? 3

URL 1/3: https://youtube.com/watch?v=dQw4w9WgXcQ
✅ URL 1 added successfully
URL 2/3: https://youtube.com/shorts/abc123
✅ URL 2 added successfully
URL 3/3: https://youtube.com/watch?v=xyz789
✅ URL 3 added successfully

💾 Save these URLs to Excel file for future use? (y/n): y
✅ URLs saved to video_links.xlsx

[1/3] Processing: https://youtube.com/watch?v=dQw4w9WgXcQ
✅ Successfully downloaded: Never Gonna Give You Up
[2/3] Processing: https://youtube.com/shorts/abc123
✅ Successfully downloaded: Funny Cat Video
[3/3] Processing: https://youtube.com/watch?v=xyz789
✅ Successfully downloaded: How to Cook Pasta

🎉 Successfully downloaded 3 videos!
```

Pretty cool, right? It shows you exactly what's happening and gives you nice checkmarks when things work!

## Want to upload videos to YouTube too?

If you want to upload your downloaded videos to your YouTube channel, here's how:

### 🔑 **Step 1: Get YouTube API credentials**

This sounds scary but it's not that hard:

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** (or use an existing one)
3. **Go to "APIs & Services" > "Credentials"**
4. **Click "Create Credentials" > "OAuth Client ID"**
5. **Choose "Desktop App"**
6. **Download the JSON file** and rename it to `youtube_credentials.json` (put it in your project folder)
7. **Enable YouTube Data API v3** in the API Library

### 🚀 **Step 2: Upload your videos**

1. **Make sure you're logged into YouTube** in your browser
2. **Run the upload script:**
   ```bash
   # Windows
   python upload_videos.py

   # Mac/Linux
   python3 upload_videos.py
   ```
3. **It will open your browser** for you to approve access
4. **Watch it upload your videos!**

## What if something goes wrong?

Don't panic! Here are solutions to common problems:

### 😵 **"yt-dlp not found"**
- **Windows:** `pip install yt-dlp`
- **Mac:** `brew install yt-dlp` or `pip3 install yt-dlp`
- **Linux:** `sudo apt install yt-dlp` or `pip3 install yt-dlp`

### 😵 **"No module named 'pandas'"**
- Run: `python3 install_dependencies.py`
- Or manually: `pip install pandas pathvalidate openpyxl`

### 😵 **"Permission denied"**
- Try: `pip install --user pandas pathvalidate yt-dlp openpyxl`
- Or create a virtual environment (Google "Python virtual environment" if you're curious)

### 😵 **Downloads fail**
- Check your internet connection
- Some videos might be region-restricted
- Try a different video to test

### 😵 **"Can't find video_links.xlsx"**
- Either create the Excel file manually
- Or just use option 2 (terminal input) - it's easier anyway!

## What's in this folder?

After you download everything, you'll see these files:

```
youtube_automation/
├── downloads/              # Your downloaded videos end up here
├── download_videos.py      # The main script you run
├── upload_videos.py        # For uploading to YouTube
├── video_links.xlsx        # Excel file with your URLs (if you use it)
├── youtube_credentials.json # Your YouTube API credentials (you create this)
├── config.py              # Settings you can change
└── Other files...         # Boring technical stuff
```

**Important:** The `youtube_credentials.json` file is not included in this repository for security reasons. You need to create it yourself following the YouTube API setup instructions above.

### 🔧 **Setting up credentials**

1. **Copy the template file:**
   ```bash
   cp youtube_credentials.json.template youtube_credentials.json
   ```

2. **Edit the file** and replace the placeholder values with your actual Google OAuth credentials:
   - Replace `YOUR_CLIENT_ID_HERE` with your actual client ID
   - Replace `YOUR_PROJECT_ID_HERE` with your actual project ID
   - Replace `YOUR_CLIENT_SECRET_HERE` with your actual client secret

3. **Never commit this file** - it's already in `.gitignore` to prevent accidental commits

## A few important notes

- **Be respectful:** Only download videos you have permission to download
- **Copyright matters:** Don't re-upload copyrighted content without permission
- **This is for personal/educational use:** Please respect YouTube's terms of service
- **Having issues?** Feel free to ask for help!

---

## That's it! 🎉

You now have a super easy way to download YouTube videos in bulk. Whether you're a content creator, student, or just someone who likes to have videos saved locally, this tool should make your life easier.

**Quick recap:**
1. Install Python and the required packages
2. Run `python3 download_videos.py` (or `python download_videos.py` on Windows)
3. Choose how you want to input your URLs
4. Watch the magic happen!

**Questions? Issues?** Feel free to ask for help. We've all been there - technology can be frustrating sometimes, but once you get it working, it's pretty awesome!

**Happy downloading!** 📺✨

---
*Version 1.0.0 - Made with ❤️ for people who just want to download some videos without the hassle*
