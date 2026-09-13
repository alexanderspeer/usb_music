from pathlib import Path
import shutil
import sys

import yt_dlp


LINKS_FILE = "youtube_links.txt"
OUTPUT_FOLDER = "downloaded_music"
ARCHIVE_FILE = "downloaded_archive.txt"


def main():
    base_dir = Path(__file__).resolve().parent
    links_path = base_dir / LINKS_FILE
    output_dir = base_dir / OUTPUT_FOLDER
    archive_path = base_dir / ARCHIVE_FILE

    if not links_path.exists():
        print(f'Error: Could not find "{LINKS_FILE}" in:')
        print(base_dir)
        sys.exit(1)

    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg is not installed or is not available on your PATH.")
        print("ffmpeg is required to convert downloaded audio to MP3.")
        print("Install ffmpeg, then run this script again.")
        sys.exit(1)

    links = [
        line.strip()
        for line in links_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    if not links:
        print(f'No links found in "{LINKS_FILE}".')
        return

    output_dir.mkdir(exist_ok=True)

    ydl_options = {
        # Download the best available audio stream.
        "format": "bestaudio/best",

        # Save files into downloaded_music/.
        "outtmpl": str(output_dir / "%(title)s [%(id)s].%(ext)s"),

        # Convert the audio to MP3.
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",  # Best VBR quality.
            }
        ],

        # Prevent a video URL containing a playlist parameter from
        # unexpectedly downloading the entire playlist.
        "noplaylist": True,

        # Record successful downloads so rerunning the script skips them.
        "download_archive": str(archive_path),

        # Continue to the next URL if one download fails.
        "ignoreerrors": True,

        # Use a clean filename on Windows/macOS/Linux.
        "windowsfilenames": True,
    }

    print(f"Found {len(links)} link(s).")
    print(f"Saving MP3 files to: {output_dir}")
    print()

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(links)

    print()
    print("Finished.")


if __name__ == "__main__":
    main()
