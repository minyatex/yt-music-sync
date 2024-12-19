#!/usr/bin/env python3

import os
from pathlib import Path
from yt_dlp import YoutubeDL

# Configuration
PLAYLIST_URLS_FILE = '/Users/tsuki/yt playlist sync/playlist_urls.txt'
DOWNLOAD_ARCHIVE_FILE = '/Users/tsuki/yt playlist sync/archive.txt'
LOCAL_PLAYLISTS_DIR = '/Users/tsuki/yt playlist sync/Playlists'

def read_playlist_urls(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def main():
    # Ensure the local playlists directory exists
    if not Path(LOCAL_PLAYLISTS_DIR).is_dir():
        os.makedirs(LOCAL_PLAYLISTS_DIR)
    # Check if the playlist URLs file exists
    if not Path(PLAYLIST_URLS_FILE).is_file():
        print(f"Playlist URLs file not found: {PLAYLIST_URLS_FILE}")
        return

    # Read playlist URLs
    playlist_urls = read_playlist_urls(PLAYLIST_URLS_FILE)
    if not playlist_urls:
        print("No playlist URLs found.")
        return

    # yt-dlp options
    ydl_opts = {
        'cookiesfrombrowser': ('chrome', 'Default', None, None),
        'format': 'm4a', 
        'extractaudio': True,  # Equivalent to -x
        'embedmetadata': True,  # Equivalent to --embed-metadata
        'writethumbnail': True,  # Necessary for --embed-thumbnail
        'outtmpl': os.path.join(LOCAL_PLAYLISTS_DIR, '%(playlist_title)s', '%(title)s - %(channel)s - %(id)s.%(ext)s'),
        'download_archive': DOWNLOAD_ARCHIVE_FILE,

        'ignoreerrors': 'only_download',
        # 'outtmpl': {'pl_thumbnail': ''},
        'postprocessor_args': {'thumbnailsconvertor+ffmpeg_o': ['-c:v',
                                                                'png',
                                                                '-vf',
                                                                'crop=ih']},
        'postprocessors': [{'key': 'FFmpegExtractAudio',
                            'nopostoverwrites': False,
                            'preferredcodec': 'best',
                            'preferredquality': '5'},
                            {'add_chapters': True,
                            'add_infojson': 'if_exists',
                            'add_metadata': True,
                            'key': 'FFmpegMetadata'},
                            {'already_have_thumbnail': False, 'key': 'EmbedThumbnail'},
                            {'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],

        'writethumbnail': True}

    # Download each playlist
    with YoutubeDL(ydl_opts) as ydl:
        for playlist_url in playlist_urls:
            print(f"Downloading playlist: {playlist_url}")
            ydl.download([playlist_url])

    print("Download complete.")

if __name__ == '__main__':
    main()
