import yt_dlp
import json
import sys
from pathlib import Path


def get_video_captions(youtube_url, language='en'):
    """
    Extract captions from a YouTube video using yt-dlp
    
    Args:
        youtube_url (str): The YouTube video URL
        language (str): Language code for captions (default: 'en')
    
    Returns:
        str: The extracted captions text
    """
    
    # Configure yt-dlp options
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [language],
        'skip_download': True,
        'subtitlesformat': 'vtt',
        'outtmpl': 'temp_subtitle'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info
            info = ydl.extract_info(youtube_url, download=False)
            video_title = info.get('title', 'Unknown')
            
            print(f"Video Title: {video_title}")
            
            # Check if captions are available
            subtitles = info.get('subtitles', {})
            automatic_captions = info.get('automatic_captions', {})
            
            if language in subtitles:
                print(f"Manual captions found in {language}")
                # Download manual captions
                ydl_opts['writesubtitles'] = True
                ydl_opts['writeautomaticsub'] = False
            elif language in automatic_captions:
                print(f"Automatic captions found in {language}")
                # Download automatic captions
                ydl_opts['writesubtitles'] = False
                ydl_opts['writeautomaticsub'] = True
            else:
                available_langs = list(subtitles.keys()) + list(automatic_captions.keys())
                print(f"No captions found in {language}")
                print(f"Available languages: {available_langs}")
                return None
            
            # Download captions
            with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                ydl_download.download([youtube_url])
            
            # Find and read the downloaded caption file
            caption_files = list(Path('.').glob(f'temp_subtitle.{language}.vtt'))
            if not caption_files:
                print("Caption file not found after download")
                return None
            
            caption_file = caption_files[0]
            captions_text = parse_vtt_file(caption_file)
            
            # Clean up the temporary file
            caption_file.unlink()
            
            return captions_text
            
    except Exception as e:
        print(f"Error extracting captions: {str(e)}")
        return None


def parse_vtt_file(vtt_file_path):
    """
    Parse VTT file and extract clean text
    
    Args:
        vtt_file_path (Path): Path to the VTT file
    
    Returns:
        str: Clean caption text
    """
    try:
        with open(vtt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        captions = []
        skip_next = False
        
        for line in lines:
            line = line.strip()
            
            # Skip VTT header and timestamp lines
            if line.startswith('WEBVTT') or line.startswith('NOTE') or '-->' in line or line == '':
                continue
            
            # Skip lines that look like timestamps
            if line.replace(':', '').replace('.', '').replace(',', '').isdigit():
                continue
            
            # Add non-empty text lines
            if line and not line.startswith('<'):
                captions.append(line)
        
        return '\n'.join(captions)
        
    except Exception as e:
        print(f"Error parsing VTT file: {str(e)}")
        return None


def main():
    """
    Main function to demonstrate caption extraction
    """
    # YouTube URL variable
    youtube_url = "https://www.youtube.com/watch?v=yAj5EnyuakI"
    
    # You can also accept URL from command line arguments if needed
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
    
    if not youtube_url:
        print("Please provide a YouTube URL")
        return
    
    # Get language preference (default to English)
    language = 'en'  # You can change this to any language code you prefer
    
    print(f"\nExtracting captions from: {youtube_url}")
    print(f"Language: {language}")
    print("-" * 50)
    
    captions = get_video_captions(youtube_url, language)
    
    if captions:
        print("\n=== CAPTIONS ===")
        print(captions)
        
        # Optionally save to file
        save_to_file = input("\nSave captions to file? (y/n): ").strip().lower()
        if save_to_file == 'y':
            filename = f"captions_{language}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(captions)
            print(f"Captions saved to: {filename}")
    else:
        print("Failed to extract captions")


if __name__ == "__main__":
    main()