# Twitch Video Downloader 🎬

Advanced Python script for downloading videos, VODs, and clips from Twitch.tv platform. Utilizes the `yt-dlp` library for reliable content downloading with various quality options and metadata support.

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed Usage](#-detailed-usage)
- [Supported Formats](#-supported-formats)
- [Quality Options](#-quality-options)
- [File Structure](#-file-structure)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Examples](#-examples)

## 🚀 Installation

### System Requirements

- Python 3.11 or newer
- Operating System: Windows, macOS, Linux
- Internet connection

### Installing Dependencies

```bash
pip install yt-dlp
```

### Downloading the Script

1. Copy the script code to a file named `twitch_downloader.py`
2. Grant execution permissions (Linux/macOS):
   ```bash
   chmod +x twitch_downloader.py
   ```

## ⚡ Quick Start

### Interactive Mode
```bash
python twitch_downloader.py
```

### Command Line Arguments
```bash
# Basic usage
python twitch_downloader.py "https://www.twitch.tv/videos/2465592622"

# With specific quality
python twitch_downloader.py "https://www.twitch.tv/videos/2465592622" "720p"
```

## 📖 Detailed Usage

### Interactive Mode

When running the script without arguments, you'll be prompted for:

1. **Video URL** - Paste the Twitch video link
2. **Download Quality** - Choose from available options

#### Interactive Session Example:
```
🎬 Twitch Video Downloader
==============================
Enter Twitch video URL:
URL: https://www.twitch.tv/videos/2465592622

Available qualities:
1. best (best available, max 1080p)
2. 1080p
3. 720p
4. 480p
5. 360p
6. audio (audio only)
7. best + subtitles (may cause errors)

Choose quality (1-7) or press Enter for default: 2
```

### Command Line Mode

```bash
python twitch_downloader.py [URL] [QUALITY]
```

**Parameters:**
- `URL` - Twitch video link (required)
- `QUALITY` - Optional video quality (default: `best`)

## 🎯 Supported Formats

The script supports the following Twitch link types:

### VOD (Video on Demand)
```
https://www.twitch.tv/videos/123456789
https://www.twitch.tv/username/video/123456789
```

### Clips
```
https://clips.twitch.tv/ClipName
https://www.twitch.tv/username/clip/ClipName
```

### Valid URL Examples:
- `https://www.twitch.tv/videos/2465592622`
- `https://clips.twitch.tv/FamousCleverSalamanderNotATK`
- `https://www.twitch.tv/sodapoppin/clip/PowerfulHelplessCodSSSsss`

## 🎥 Quality Options

| Option | Description | Format |
|--------|-------------|--------|
| `best` | Best available (max 1080p) | Video + Audio |
| `1080p` | Full HD (if available) | Video + Audio |
| `720p` | HD | Video + Audio |
| `480p` | SD | Video + Audio |
| `360p` | Low quality | Video + Audio |
| `audio` | Audio only | Audio only |
| `worst` | Lowest quality | Video + Audio |

### Automatic Quality Selection

The script automatically selects the best available quality within the specified limit. If you choose `1080p` but the video is only available in `720p`, it will download the `720p` version.

## 📁 File Structure

### Target Directory
By default, files are saved to the `downloads/` directory in the script's location.

### File Naming Convention
```
[Channel_Name]_[Video_Title]_[Video_ID].[extension]
```

#### Example:
```
vigoletto_⭐Join the chat! Kultowy czwartek !ETS2 !Driving !Simulator !chat !tiktok_v2465592622.mp4
```

### Additional Files

The script may create the following additional files:

- **`.info.json`** - Video metadata (title, description, statistics)
- **`.rechat.json`** - Subtitles/chat (if available and enabled)

## 🔧 Troubleshooting

### Common Errors and Solutions

#### 1. Error 404 - Video Not Found
```
❌ Video not found (404). Check if the URL is correct and the video still exists.
```

**Solution:**
- Verify URL correctness
- Check if the video still exists on Twitch
- Some old videos may be unavailable

#### 2. Error 403 - Access Denied
```
❌ Access denied (403). Video may be private or blocked.
```

**Solution:**
- Video may be private
- Streamer may have restricted access
- Try with a different video

#### 3. Subtitle Errors
```
❌ Subtitle-related error. Video may not have available subtitles.
```

**Solution:**
- Script will automatically retry without subtitles
- Use options 1-6 instead of option 7

#### 4. Missing yt-dlp Module
```
ModuleNotFoundError: No module named 'yt_dlp'
```

**Solution:**
```bash
pip install yt-dlp
```

### Debugging

To get more error information, you can run the script with additional logging:

```python
# Add at the beginning of main()
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### TwitchDownloader Class

#### `__init__(download_dir="downloads")`

Initializes the downloader with the specified target directory.

**Parameters:**
- `download_dir` (str): Target directory for downloaded files

#### `is_valid_twitch_url(url)`

Checks if the provided URL is a valid Twitch link.

**Parameters:**
- `url` (str): URL to check

**Returns:**
- `bool`: True if URL is valid

#### `get_video_info(url)`

Retrieves video information without downloading.

**Parameters:**
- `url` (str): Video URL

**Returns:**
- `dict`: Dictionary with video information or None on error

#### `download_video(url, quality='best', download_subtitles=False)`

Main method for downloading videos.

**Parameters:**
- `url` (str): Video URL
- `quality` (str): Video quality
- `download_subtitles` (bool): Whether to download subtitles

**Returns:**
- `bool`: True if download completed successfully

## 💡 Examples

### Example 1: Basic Download
```python
from twitch_downloader import TwitchDownloader

downloader = TwitchDownloader()
url = "https://www.twitch.tv/videos/2465592622"
success = downloader.download_video(url)

if success:
    print("Video downloaded successfully!")
```

### Example 2: Download with Specific Quality
```python
downloader = TwitchDownloader("./my_videos")
url = "https://www.twitch.tv/videos/2465592622"
success = downloader.download_video(url, quality="720p")
```

### Example 3: Check Information Before Download
```python
downloader = TwitchDownloader()
url = "https://www.twitch.tv/videos/2465592622"

# Check information
info = downloader.get_video_info(url)
if info:
    print(f"Title: {info['title']}")
    print(f"Duration: {info['duration']} seconds")
    
    # Download if video is shorter than 2 hours
    if info['duration'] < 7200:
        downloader.download_video(url)
```

### Example 4: Batch Download
```python
urls = [
    "https://www.twitch.tv/videos/2465592622",
    "https://clips.twitch.tv/ExampleClip",
    "https://www.twitch.tv/videos/1234567890"
]

downloader = TwitchDownloader()

for url in urls:
    if downloader.is_valid_twitch_url(url):
        print(f"Downloading: {url}")
        downloader.download_video(url, quality="720p")
    else:
        print(f"Invalid URL: {url}")
```

## 🤝 Support

### Reporting Issues

If you encounter problems:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Ensure you have the latest version of `yt-dlp`
3. Verify that the URL is correct and the video exists

### Updates

To update `yt-dlp` to the latest version:

```bash
pip install --upgrade yt-dlp
```

## ⚖️ Legal Information

- Respect copyright laws and Twitch's Terms of Service
- Only download content you have the right to access
- Do not redistribute downloaded content without permission from creators
- This script is intended for personal use only

## 📄 License

This script is provided for educational and personal use purposes. Users are responsible for complying with all applicable laws and platform terms of service.

---

**Documentation Version:** 1.0  
**Last Updated:** May 2025  
**Compatibility:** Python 3.11+, yt-dlp 2024.x+
