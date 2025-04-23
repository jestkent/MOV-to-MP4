# MOV to MP4 Converter

A simple desktop application built with Python and Tkinter that converts MOV video files to MP4 format using FFmpeg.



## Features

- Convert MOV files to MP4 format with customizable quality settings
- User-friendly graphical interface
- Progress tracking during conversion
- Quality presets (low, medium, high, original)
- Cancel conversion at any time

## Requirements

- Python 3.6 or higher
- FFmpeg (must be installed separately)
- tkinter (included with most Python installations)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/mov-to-mp4-converter.git
   cd mov-to-mp4-converter
   ```

2. **Install FFmpeg** (if not already installed)

   - **Windows**: 
     - Download from [FFmpeg's official website](https://ffmpeg.org/download.html)
     - Extract to a location on your computer (e.g., `C:\ffmpeg\`)

   - **macOS** (using Homebrew):
     ```bash
     brew install ffmpeg
     ```

   - **Linux**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

3. **Configure FFmpeg path**

   Open `converter.py` in a text editor and set the `FFMPEG_PATH` variable to point to your FFmpeg installation:

   ```python
   # *** SET THIS PATH TO YOUR FFMPEG LOCATION ***
   FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin\ffmpeg.exe"
   # If you need to manually specify ffprobe as well:
   FFPROBE_PATH = r"C:\ffmpeg\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin\ffprobe.exe"
   ```

## Usage

1. **Start the application**

   ```bash
   python converter.py
   ```

2. **Convert a MOV file**

   - Click "Browse" to select an input MOV file
   - The output file location will be automatically suggested (same directory with .mp4 extension)
   - Select your desired quality preset
   - Click "Convert" to start the conversion process
   - The progress bar will display conversion progress
   - Click "Cancel" if you need to stop the conversion

## Quality Settings

The application offers four quality presets:

- **Low**: Faster conversion, smaller file size, lower quality (CRF 28, veryfast preset)
- **Medium**: Balanced option (CRF 23, medium preset)
- **High**: Slower conversion, larger file size, higher quality (CRF 18, slow preset)
- **Original**: Lossless quality, very large file size (CRF 0, medium preset)

## Troubleshooting

- **FFmpeg not found**: Ensure the path in the script correctly points to your FFmpeg executable
- **Conversion fails**: Check if the input file is accessible and not corrupted
- **Poor quality**: Try using a higher quality preset
- **Slow conversion**: Lower quality presets convert faster

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for the fantastic video conversion tools
- Python and Tkinter for making GUI development accessible
