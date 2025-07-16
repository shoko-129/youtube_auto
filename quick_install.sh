#!/bin/bash
# Quick installation script for YouTube Automation

echo "🚀 YouTube Automation - Quick Install"
echo "====================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Try to install dependencies
echo "📦 Installing dependencies..."

# Try pip install with different methods
if pip3 install --user pandas pathvalidate yt-dlp openpyxl; then
    echo "✅ Dependencies installed successfully with --user flag"
elif pip3 install pandas pathvalidate yt-dlp openpyxl; then
    echo "✅ Dependencies installed successfully"
elif pip3 install --break-system-packages pandas pathvalidate yt-dlp openpyxl; then
    echo "✅ Dependencies installed with system override"
else
    echo "❌ Failed to install dependencies automatically"
    echo "💡 Try manual installation:"
    echo "   pip3 install --user pandas pathvalidate yt-dlp openpyxl"
    exit 1
fi

# Create sample Excel file if it doesn't exist
if [ ! -f "video_links.xlsx" ]; then
    echo "📄 Creating sample video_links.xlsx..."
    python3 -c "
import pandas as pd
df = pd.DataFrame({'Link': [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/shorts/example1',
    'https://www.youtube.com/shorts/example2'
]})
df.to_excel('video_links.xlsx', index=False)
print('✅ Sample video_links.xlsx created')
"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit video_links.xlsx with your YouTube URLs"
echo "2. Run: python3 download_videos.py"
echo ""
echo "🔧 For configuration options, edit config.py"
