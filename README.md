# 🎬 VibeItihaas AI — Automated Studio Ghibli Short Video Generator

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-9.0%2B-orange.svg)](https://ffmpeg.org/)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://github.com/openai/whisper)
[![Aspect Ratio](https://img.shields.io/badge/Format-9%3A16%20Vertical%20Shorts-purple.svg)]()
[![Platform](https://img.shields.io/badge/Tested%20on-macOS%20Apple%20Silicon-black.svg)]()

An autonomous, production-grade local script-to-video rendering pipeline built for **YouTube Shorts**, **Instagram Reels**, and **TikTok**. 

Give it an `.mp3` voiceover file, and it automatically handles transcription, timestamp extraction, visual multi-angle choreography, atmospheric particle effects (God rays, glowing Kami spiritual embers, blizzards), kinetic word-by-word captions, and exports a finished 1080x1920 MP4 short alongside a complete viral metadata package.

---

## ✨ Key Features

- **🎨 Studio Ghibli Cinematic Aesthetic**: Hand-painted atmospheric anime visual style with multi-angle camera panning and dynamic zoom choreography.
- **⚡ Ultra-Fast Local Rendering**: Streams raw RGB frame buffers directly into an optimized FFmpeg C-pipe, clocking **45–60 FPS** on Apple Silicon (renders a full 73-second short in under 50 seconds) with zero cloud GPU fees.
- **🎙️ Word-Level Kinetic Subtitles**: Powered by local OpenAI Whisper for exact timing. Uses an auto-scaling safe-margin algorithm (`MAX_SAFE_W = 900px`) that prevents long words or phrases from clipping the edges of mobile screens.
- **✨ Volumetric Atmospheric VFX**: Real-time programmatic particle simulation including floating golden Kami embers, atmospheric God Rays, blizzard streaks, and vignette grading.
- **📝 Automated Viral Metadata Generation**: Each rendered video automatically generates a companion `<name>_metadata.txt` containing:
  - 4 High-CTR clickbait & mystery titles for YouTube Shorts & Reels.
  - Ready-to-copy Instagram caption with narrative hooks, hashtags, and comment triggers.
  - YouTube SEO description, tags, and pinned comment prompts.
- **🛡️ Asset Resilience & Safe Branding**: Brand logo (`logo.png`) is preserved in the root directory so you can delete artwork in `assets/` to save disk space anytime without breaking channel branding. If artworks are missing, procedural atmospheric watercolor canvases kick in automatically.

---

## 📁 Project Directory Structure

```text
ytshorts/
├── input/                          # 📥 Place your raw voiceover .mp3 files here
│   └── .gitkeep
├── output/                         # 📤 Rendered .mp4 videos and companion _metadata.txt
│   └── .gitkeep
├── assets/                         # 🎨 Master Studio Ghibli art files (safe to clear for space)
│   ├── ghibli_01_everest_*.jpg
│   ├── ghibli_02_kailash_*.jpg
│   └── ghibli_03_axis_mundi_*.jpg
├── generate_reel.py                # 🚀 Master video compilation & rendering engine
├── viral_research_and_scripts.txt  # 📜 Viral script repository & deep research bank
├── logo.png                        # 🔱 Your channel brand badge (vibeitihaas)
├── requirements.txt                # 📦 Python dependencies
├── .gitignore                      # 🙈 Keeps raw MP3s and MP4s off GitHub
└── README.md                       # 📖 Documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Ensure you have **Python 3.10+** and **FFmpeg** installed on your system.

On macOS (via Homebrew):
```bash
brew install ffmpeg
```

On Ubuntu / Debian:
```bash
sudo apt update && sudo apt install ffmpeg python3-venv
```

---

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AaradhyaproK/ytshorts.git
   cd ytshorts
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### 3. Generate a Video Short

1. **Add your audio file:**
   Drop your voiceover audio file (e.g. `kailash.mp3`) into the `input/` folder:
   ```text
   input/your_audio.mp3
   ```

2. **Run the master production script:**
   ```bash
   python3 generate_reel.py
   ```
   *Or specify a custom audio file directly:*
   ```bash
   python3 generate_reel.py --input input/your_audio.mp3
   ```

3. **Check your output:**
   Once completed, open the `output/` directory:
   - `output/<name>_ghibli_reel.mp4` — Your final 1080x1920 9:16 vertical video.
   - `output/<name>_metadata.txt` — Your ready-to-use YouTube & Instagram titles, captions, and hashtags.

---

## 🛠️ Customization

### Change Brand Name & Logo
- Replace `logo.png` in the root directory with your own square or transparent PNG logo.
- To change the display name (default: `vibeitihaas`), edit line 249 of `generate_reel.py`:
  ```python
  d_brand.text((pill_x + 82, pill_y + 20), "yourchannel", fill=(255, 255, 255, 255), font=font_brand)
  ```

### Change Video Resolution or FPS
In `generate_reel.py`:
```python
W, H = 1080, 1920    # Vertical 9:16 aspect ratio
FPS = 30             # Frame rate
MAX_SAFE_W = 900     # Ensures >= 90px margin on left & right
```

---

## 📜 Viral Script & Research Vault

Looking for inspiration or viral video ideas? Open **`viral_research_and_scripts.txt`** for:
- The 4-pillar retention framework (3-second hook, curiosity gap, loop transition, comment bait).
- Ready-to-record 60-70 second scripts on:
  - **Dwarka**: The 9,000-year-old underwater metropolis.
  - **Ellora Kailasa Temple**: The monolithic temple carved top-down from 400,000 tons of rock.
  - **Konark Sun Temple**: The 52-ton levitating magnet idol.
  - **Ram Setu**: The NASA satellite scan and floating pumice stones.
  - **Lepakshi Temple**: The gravity-defying hanging pillar.

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details. Built with ❤️ for content creators and digital storytellers by **@vibeitihaas**.
