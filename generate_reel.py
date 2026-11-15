#!/usr/bin/env python3
"""
vibeitihaas Automated Studio Ghibli Short Video Generator
Pipeline: MP3 in input/ -> Whisper Transcription -> Ghibli Cinematic Visuals -> Kinetic Subtitles -> MP4 in output/
"""

import os
import sys
import glob
import math
import subprocess
import time
import random
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
MAX_SAFE_W = 900  # Enforces at least 90px safe padding on both left and right

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
ASSETS_DIR = os.path.join(SCRIPT_DIR, "assets")

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    out = subprocess.check_output(cmd).decode().strip()
    return float(out)

def load_and_prep(img_path):
    img = Image.open(img_path).convert('RGB')
    bw, bh = img.size
    scale = max(W / bw, H / bh) * 1.25  # Extra margin for deep cinematic zooms & pans
    nw, nh = int(bw * scale), int(bh * scale)
    return img.resize((nw, nh), Image.Resampling.LANCZOS)

def load_asset_or_fallback(pattern, top_rgb, bot_rgb):
    """Loads image from assets/ or generates procedural Ghibli watercolor if assets were cleared for space."""
    files = sorted(glob.glob(pattern))
    if files:
        return load_and_prep(files[-1])
    
    # Procedural Ghibli atmospheric watercolor canvas
    base = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(base)
    for y in range(H):
        r = y / H
        col = (
            int(top_rgb[0] * (1 - r) + bot_rgb[0] * r),
            int(top_rgb[1] * (1 - r) + bot_rgb[1] * r),
            int(top_rgb[2] * (1 - r) + bot_rgb[2] * r)
        )
        draw.line([(0, y), (W, y)], fill=col)
    scale = 1.25
    return base.resize((int(W * scale), int(H * scale)), Image.Resampling.LANCZOS)

def transcribe_audio(audio_path, cache_json):
    if os.path.exists(cache_json):
        print(f"[Whisper] Using cached transcription: {cache_json}")
        with open(cache_json, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"[Whisper] Transcribing {os.path.basename(audio_path)} with word timestamps...")
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)
    with open(cache_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[Whisper] Saved transcript to {cache_json}")
    return result

def generate_metadata_package(audio_basename, transcript, output_path):
    """Automatically generates High-CTR titles, Instagram caption, and YouTube description/tags."""
    # Check if a custom metadata exists for kailash, otherwise synthesize dynamically
    if audio_basename.lower() == "kailash" and os.path.exists(output_path):
        return

    if "abhimayu" in audio_basename.lower() or "abhimanyu" in audio_basename.lower():
        content = f"""================================================================================
⚡ VIBEITIHAAS VIRAL METADATA PACKAGE
🎬 Video: {audio_basename}_ghibli_reel.mp4
📌 Topic: Day 13 of Kurukshetra: Abhimanyu's Chakravyuha
================================================================================

--------------------------------------------------------------------------------
🔥 1. HIGH-CTR TITLES (Select for YouTube Shorts & Reels)
--------------------------------------------------------------------------------
Option 1 (Shock & Paradox):
16-Year-Old vs 7 Maharathis: The Day Dharma Died ⚔️🩸

Option 2 (Strategy & Mystery):
How 1 Boy Broke The Impossible Chakravyuha 👁️ Mahabharata Secret

Option 3 (Moral Conflict):
Why Drona & Karna Broke All War Rules Against Abhimanyu? 😱

--------------------------------------------------------------------------------
📸 2. INSTAGRAM REELS CAPTION (Ready to Copy-Paste)
--------------------------------------------------------------------------------
Kauravon ne Chakravyuha ladayi jeetne ke liye nahi... balki Pandavon ki will-power ko hamesha ke liye todne ke liye design kiya tha. ⚔️🩸

Day 13 of Kurukshetra: Guru Drona ki sabse calculated military formation ke saamne khada tha ek 16 saal ka ladka, jisne akele Kaurav sena ke 6 defense layers ko collapse kar diya!

Lekin jab Kauravon ko apni haar dikhne lagi, to unhone ancient warfare ke saare codes tod diye...

👇 Kya Karna aur Drona ka Abhimanyu ko milkar gherna justified tha? Tell us your opinion in the comments!

Save this reel & share with history lovers! 📲
Follow @vibeitihaas for untold historical & epic breakdowns.

.
.
#vibeitihaas #mahabharata #abhimanyu #kurukshetra #chakravyuha #sanatandharma #ancienthistory #shorts #viralreels

--------------------------------------------------------------------------------
📺 3. YOUTUBE SHORTS DESCRIPTION (SEO & Algorithm Optimized)
--------------------------------------------------------------------------------
Day 13 of Kurukshetra: Guru Drona created the lethal 7-tier Chakravyuha to psychologically break the Pandavas. But 16-year-old warrior Abhimanyu breached 6 concentric defense tiers alone. Why did the greatest Maharathis break all rules of warfare to defeat one teenager?

⚔️ Comment your thoughts on Abhimanyu's valor!
🔔 Subscribe to @vibeitihaas for deep epic & historical breakdowns.

#Shorts #Mahabharata #Abhimanyu #Chakravyuha #vibeitihaas #Kurukshetra #AncientHistory #SanatanDharma

--------------------------------------------------------------------------------
💬 4. PINNED COMMENT STRATEGY
--------------------------------------------------------------------------------
"Kya Karna aur Drona ka Abhimanyu ko akele gherna justified tha ya unka sabse bada moral downfall? Apni ray comment mein batayein! 👇⚔️"

--------------------------------------------------------------------------------
🏷️ 5. SEARCH KEYWORDS / TAGS
--------------------------------------------------------------------------------
abhimanyu chakravyuha mystery, day 13 kurukshetra war, how abhimanyu broke chakravyuha, mahabharata breakdown in hindi, vibeitihaas, why karna killed abhimanyu, guru drona chakravyuha strategy, viral shorts
================================================================================
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return

    if "zoho" in audio_basename.lower() or "vembu" in audio_basename.lower():
        content = f"""================================================================================
⚡ VIBEITIHAAS VIRAL METADATA PACKAGE
🎬 Video: {audio_basename}_ghibli_reel.mp4
📌 Topic: Sridhar Vembu (Zoho) — The Village Founder Who Refused Billions
================================================================================

--------------------------------------------------------------------------------
🔥 1. HIGH-CTR TITLES (Select for YouTube Shorts & Reels)
--------------------------------------------------------------------------------
Option 1 (Extreme Paradox):
Rejected Silicon Valley Billions to Build a Tech Empire in a Village! 🚜💻

Option 2 (Emotional Curiosity):
Why This Indian Billionaire Wears Dhoti & Rides a Cycle? 🇮🇳 Zoho Story

Option 3 (Shock Value):
$0 VC Funding, $1 Billion Pure Profit: The Swadeshi Genius! 💰🔥

--------------------------------------------------------------------------------
📸 2. INSTAGRAM REELS CAPTION (Ready to Copy-Paste)
--------------------------------------------------------------------------------
Silicon Valley ke investors ne hazaaron crore ke cheques offer kiye... lekin is Indian visionary ne unke dollar cheques unke munh par wapas kar diye! 🚜💻🇮🇳

Zero Venture Capital. Zero Debt. Zero Layoffs.

Sridhar Vembu ne California ka corporate glamour chhod kar Tamil Nadu ke chhote se gao Mathalamparai mein Zoho ka global empire khada kar diya. Gaon ke un bachhon ko Zoho Schools mein train kiya jinhe college naseeb nahi hua tha—aur aaj wahi rural coders Google aur Microsoft ke software ko takkar de rahe hain! 

"Real wealth is not valuation hype; it's creating prosperity where people are." ✨

👇 Desi Swadeshi success ke samman mein comment mein likhein:
"PROUD INDIAN" 🇮🇳

Save this reel for pure entrepreneurial inspiration! 📲
Follow @vibeitihaas for untold stories of Indian legends & visionary builders.

.
.
#vibeitihaas #sridharvembu #zoho #startupindia #swadeshi #entrepreneurship #indianstartups #inspiration #businesscasestudy #successmindset #shorts #viralreels

--------------------------------------------------------------------------------
📺 3. YOUTUBE SHORTS DESCRIPTION (SEO & Algorithm Optimized)
--------------------------------------------------------------------------------
While modern tech startups burn thousands of crores in VC funding, Sridhar Vembu built Zoho with $0 outside funding, profitable from day one, headquartered in a small rural village in Tamil Nadu! He proved that rural Indian youth can outcode Silicon Valley giants.

🇮🇳 Type "PROUD INDIAN" in the comments if you support Swadeshi tech!
🔔 Subscribe to @vibeitihaas for deep dives into Indian history, business, and visionary leaders.

#Shorts #Zoho #SridharVembu #StartupIndia #vibeitihaas #BusinessCaseStudy #Entrepreneurship #Swadeshi #IndianTech

--------------------------------------------------------------------------------
💬 4. PINNED COMMENT STRATEGY
--------------------------------------------------------------------------------
"Western valuation hype aur massive layoffs ya asli Swadeshi profit? Sridhar Vembu ke is visionary vision ke baare mein aapki kya ray hai? Comment karein! 👇🇮🇳"

--------------------------------------------------------------------------------
🏷️ 5. SEARCH KEYWORDS / TAGS
--------------------------------------------------------------------------------
sridhar vembu zoho case study, zoho founder story hindi, rural india tech revolution, swadeshi startup, bootstrapped billionaire, vibeitihaas, startup india inspiration, shorts
================================================================================
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return

    title_topic = audio_basename.replace("_", " ").title()
    
    if "kailash" in audio_basename.lower():
        cta_word = "HAR HAR MAHADEV"
        deity_tag = "#mahadev #shiva #kedarnath #bholenath"
        theme_tag = "#kailashparvat #mountkailash #axismundi"
    elif "dwarka" in audio_basename.lower():
        cta_word = "JAI SHREE KRISHNA"
        deity_tag = "#krishna #shreekrishna #dwarkadhish"
        theme_tag = "#dwarka #underwatercity #ancientdwarka"
    elif "ram" in audio_basename.lower() or "setu" in audio_basename.lower():
        cta_word = "JAI SHREE RAM"
        deity_tag = "#ram #shreeram #ayodhya #hanuman"
        theme_tag = "#ramsetu #adamsbridge #floatingstones"
    elif "ellora" in audio_basename.lower():
        cta_word = "HAR HAR MAHADEV"
        deity_tag = "#mahadev #shiva #ancienttemple"
        theme_tag = "#ellora #kailasatemple #ancientengineering"
    elif "konark" in audio_basename.lower():
        cta_word = "JAI SURYA DEV"
        deity_tag = "#suryadev #sun #ancienttemple"
        theme_tag = "#konark #suntemple #electromagnetic"
    elif "vault" in audio_basename.lower() or "padmanabh" in audio_basename.lower():
        cta_word = "OM NAMO NARAYANAYA"
        deity_tag = "#vishnu #narayana #padmanabhaswamy #ancientindia"
        theme_tag = "#vaultb #nagabandham #acousticlock #mystery"
    elif "chanakya" in audio_basename.lower() or "vishkanya" in audio_basename.lower():
        cta_word = "CHANAKYA NITI"
        deity_tag = "#chanakya #takshashila #maurya #ancientindia"
        theme_tag = "#geopolitics #intelligence #vishkanya #historyfacts"
    elif "lepakshi" in audio_basename.lower():
        cta_word = "HAR HAR MAHADEV"
        deity_tag = "#veerabhadra #shiva #mahadev #sanatandharma"
        theme_tag = "#lepakshi #hangingpillar #antigravity #ancienttemple"
    else:
        cta_word = "SANATAN DHARMA"
        deity_tag = "#bharat #sanatandharma #incredibleindia"
        theme_tag = f"#{audio_basename.lower().replace(' ', '')} #mystery #ancienthistory"

    content = f"""================================================================================
⚡ VIBEITIHAAS VIRAL METADATA PACKAGE
🎬 Video: {audio_basename}_ghibli_reel.mp4
📌 Topic: {title_topic}
================================================================================

--------------------------------------------------------------------------------
🔥 1. HIGH-CTR TITLES (Select for YouTube Shorts & Reels)
--------------------------------------------------------------------------------
Option 1 (Mystery Hook):
The Unsolved Mystery of {title_topic}! 😱 Science Ke Paas Koi Jawab Nahi!

Option 2 (Question / Curiosity):
{title_topic} Ka Khaufnak Sach! 👁️ Ancient Indian Secrets Exposed

Option 3 (Shocking Paradox):
NASA & Scientists Shocked by {title_topic}! ⏳ Real History of Bharat

--------------------------------------------------------------------------------
📸 2. INSTAGRAM REELS CAPTION (Ready to Copy-Paste)
--------------------------------------------------------------------------------
Kya aapko pata hai ki {title_topic} ke peeche ka asli rahasya kya hai? 🌌⚡

Hamare pracheen Bharat mein aisi divya technology aur itihaas chupa hai jisne modern science ko bhi hairan kar diya hai! Aisi azeeb ghatnayein aur architectural miracles jo aaj ke modern yug mein bhi namumkin maani jaati hain.

👇 Hamare is divya itihaas ke samman mein comment mein likhein:
"{cta_word}" 🙏🔱

Follow 👉 @vibeitihaas for more untold mysteries of Indian history & Sanatan culture!
Save this reel & share with your friends! 📲

.
.
#vibeitihaas #{audio_basename.lower().replace('_', '')} {theme_tag} {deity_tag} #ancientindia #indianhistory #sanatandharma #mystery #viralreels #reelsindia #shorts #trending

--------------------------------------------------------------------------------
📺 3. YOUTUBE SHORTS DESCRIPTION (SEO & Algorithm Optimized)
--------------------------------------------------------------------------------
Discover the mind-bending mystery of {title_topic} with @vibeitihaas. Ancient Indian history holds engineering marvels and cosmic secrets that baffle modern archeology even today!

🔱 Comment '{cta_word}' to celebrate our ancient civilization!
🔔 Subscribe to @vibeitihaas for daily historical mysteries and untold Sanatan secrets.

#Shorts #{audio_basename.replace('_', '')} #vibeitihaas #IndianHistory #SanatanDharma #AncientMysteries #Trending

--------------------------------------------------------------------------------
💬 4. PINNED COMMENT STRATEGY (Boosts Comment Algorithm)
--------------------------------------------------------------------------------
"Kya aapko {title_topic} ke is rahasya ke baare mein pehle se pata tha? Apni ray comment mein zaroor batayein aur '{cta_word}' likhein! 👇🔱"

--------------------------------------------------------------------------------
🏷️ 5. SEARCH KEYWORDS / TAGS
--------------------------------------------------------------------------------
{audio_basename.replace('_', ' ')} mystery, {audio_basename.replace('_', ' ')} in hindi, vibeitihaas, ancient indian mysteries, sanatan dharma secrets, viral shorts, ghibli reel
================================================================================
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Generate Ghibli Reel for vibeitihaas")
    parser.add_argument("--input", "-i", type=str, default=None, help="Path to input .mp3 file")
    args = parser.parse_args()

    # Determine input audio
    if args.input:
        audio_file = args.input
    else:
        mp3s = sorted(glob.glob(os.path.join(INPUT_DIR, "*.mp3")), key=os.path.getmtime)
        if not mp3s:
            print(f"[Error] No .mp3 files found in {INPUT_DIR}/. Please place your audio file there.")
            sys.exit(1)
        audio_file = mp3s[-1]

    audio_basename = os.path.splitext(os.path.basename(audio_file))[0]
    output_file = os.path.join(OUTPUT_DIR, f"{audio_basename}_ghibli_reel.mp4")

    print("=======================================================")
    print("  vibeitihaas Studio Ghibli Reel Generator")
    print(f"  Input:  {audio_file}")
    print(f"  Output: {output_file}")
    print("=======================================================")

    duration = get_audio_duration(audio_file)
    total_frames = int(duration * FPS) + 1
    print(f"Audio Duration: {duration:.2f}s ({total_frames} frames @ {FPS} FPS)")

    # Load 3 Ghibli Master Artworks (or safe procedural fallbacks if assets folder was cleared)
    print("Loading Ghibli Master Artworks...")
    if "abhimayu" in audio_basename.lower() or "abhimanyu" in audio_basename.lower():
        assets = {
            "chakravyuha": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_01_chakravyuha*.jpg"),
                top_rgb=(20, 24, 55), bot_rgb=(235, 140, 50)
            ),
            "warrior": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_02_warrior*.jpg"),
                top_rgb=(45, 20, 25), bot_rgb=(245, 190, 80)
            ),
            "standoff": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_03_standoff*.jpg"),
                top_rgb=(20, 24, 55), bot_rgb=(235, 140, 50)
            ),
            "drona": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_04_drona*.jpg"),
                top_rgb=(25, 30, 60), bot_rgb=(240, 180, 100)
            ),
            "arjuna_distant": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_05_arjuna_distant*.jpg"),
                top_rgb=(20, 25, 45), bot_rgb=(220, 130, 60)
            ),
            "breach": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_06_breach*.jpg"),
                top_rgb=(40, 15, 20), bot_rgb=(255, 200, 80)
            ),
            "chariot_wheel": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_abhimanyu_07_chariot_wheel_climax*.jpg"),
                top_rgb=(50, 15, 25), bot_rgb=(250, 150, 60)
            ),
        }
    elif "chanakya" in audio_basename.lower() or "vishkanya" in audio_basename.lower():
        assets = {
            "alexander": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_chanakya_01_alexander*.jpg"),
                top_rgb=(40, 25, 30), bot_rgb=(240, 180, 100)
            ),
            "mastermind": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_chanakya_02_mastermind*.jpg"),
                top_rgb=(25, 20, 45), bot_rgb=(235, 140, 60)
            ),
            "vishkanya": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_chanakya_03_vishkanya*.jpg"),
                top_rgb=(30, 15, 40), bot_rgb=(200, 100, 160)
            ),
            "mutiny": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_chanakya_04_greek_mutiny*.jpg"),
                top_rgb=(15, 20, 35), bot_rgb=(60, 90, 130)
            ),
            "victory": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_chanakya_05_victory*.jpg"),
                top_rgb=(35, 15, 25), bot_rgb=(250, 160, 70)
            ),
        }
    elif "vembu" in audio_basename.lower() or "zoho" in audio_basename.lower() or "shridhar" in audio_basename.lower():
        assets = {
            "silicon_valley": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_01_silicon_valley*.jpg"),
                top_rgb=(30, 20, 45), bot_rgb=(240, 160, 80)
            ),
            "journey": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_02_journey*.jpg"),
                top_rgb=(45, 60, 95), bot_rgb=(250, 200, 120)
            ),
            "village_hq": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_03_village_hq*.jpg"),
                top_rgb=(35, 75, 45), bot_rgb=(220, 230, 140)
            ),
            "rural_coders": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_04_rural_coders*.jpg"),
                top_rgb=(40, 50, 40), bot_rgb=(240, 200, 110)
            ),
            "global_tech": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_05_global_tech*.jpg"),
                top_rgb=(15, 20, 50), bot_rgb=(70, 140, 200)
            ),
            "bicycle": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_vembu_06_bicycle_dhoti*.jpg"),
                top_rgb=(30, 70, 40), bot_rgb=(245, 215, 120)
            ),
        }
    else:
        assets = {
            "everest": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_01_everest_*.jpg"),
                top_rgb=(25, 65, 115), bot_rgb=(240, 215, 160)
            ),
            "kailash_day": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_02_kailash_*.jpg"),
                top_rgb=(40, 95, 155), bot_rgb=(18, 45, 60)
            ),
            "axis_night": load_asset_or_fallback(
                os.path.join(ASSETS_DIR, "ghibli_03_axis_mundi_*.jpg"),
                top_rgb=(5, 12, 28), bot_rgb=(10, 25, 45)
            ),
        }

    # Transcribe
    cache_json = os.path.join(SCRIPT_DIR, f"transcript_{audio_basename}.json")
    if not os.path.exists(cache_json) and os.path.exists("transcript.json") and audio_basename == "kailash":
        cache_json = "transcript.json"
    transcript = transcribe_audio(audio_file, cache_json)

    # Multi-scene schedule mapping across the Ghibli Masterpieces
    if "abhimayu" in audio_basename.lower() or "abhimanyu" in audio_basename.lower():
        scenes_meta = [
            {"start": 0.00,  "end": 6.54,  "asset": "chakravyuha",    "zoom": (1.00, 1.15), "pan": (0.50, 0.45), "vfx": "particles"},
            {"start": 6.54,  "end": 15.80, "asset": "drona",          "zoom": (1.05, 1.22), "pan": (0.50, 0.40), "vfx": "godrays"},
            {"start": 15.80, "end": 21.20, "asset": "arjuna_distant", "zoom": (1.00, 1.18), "pan": (0.44, 0.52), "vfx": "mist"},
            {"start": 21.20, "end": 26.64, "asset": "warrior",        "zoom": (1.00, 1.20), "pan": (0.50, 0.48), "vfx": "golden_aura"},
            {"start": 26.64, "end": 35.66, "asset": "breach",         "zoom": (1.05, 1.28), "pan": (0.48, 0.42), "vfx": "particles"},
            {"start": 35.66, "end": 44.46, "asset": "standoff",       "zoom": (1.00, 1.18), "pan": (0.50, 0.40), "vfx": "particles"},
            {"start": 44.46, "end": max(duration, 51.5), "asset": "chariot_wheel", "zoom": (1.10, 1.28), "pan": (0.50, 0.42), "vfx": "golden_aura"},
        ]
        captions = [
            (0.00, 3.04, ["KAURAVON NE", "CHAKRAVYUHA"], [(0.00, 1.40), (1.40, 3.04)]),
            (3.04, 6.54, ["PSYCHOLOGICALLY", "TODNE KE LIYE!"], [(3.04, 4.80), (4.80, 6.54)]),
            (6.54, 8.48, ["GURU DRONA", "JAANTE THE KI..."], [(6.54, 7.50), (7.50, 8.48)]),
            (8.48, 11.92, ["SIRF ARJUNA AUR", "KRISHNA KE PAAS"], [(8.48, 10.20), (10.20, 11.92)]),
            (11.92, 15.80, ["7-TIER ROTATING", "DEATH MAZE FORMULA!"], [(11.92, 13.80), (13.80, 15.80)]),
            (15.80, 18.50, ["ISLIYE ARJUNA KO", "YUDDHA SE..."], [(15.80, 17.10), (17.10, 18.50)]),
            (18.50, 21.20, ["20 KILOMETER DOOR", "DIVERT KIYA!"], [(18.50, 19.80), (19.80, 21.20)]),
            (21.20, 23.54, ["LEKIN 16 SAAL KE", "ABHIMANYU NE..."], [(21.20, 22.30), (22.30, 23.54)]),
            (23.54, 26.64, ["AKELE 6 CONCENTRIC", "CIRCLES CHEER DIYE!"], [(23.54, 25.10), (25.10, 26.64)]),
            (26.64, 30.02, ["JAB KAURAVON NE DEKHA", "EK AKELA BACHHA..."], [(26.64, 28.30), (28.30, 30.02)]),
            (30.02, 33.44, ["MILITARY PRESTIGE", "MITTI MEIN MILA RAHA HAI!"], [(30.02, 31.70), (31.70, 33.44)]),
            (33.44, 35.66, ["TO UNKE HATH-PAAON", "PHOOL GAYE!"], [(33.44, 34.50), (34.50, 35.66)]),
            (35.66, 37.80, ["DRONA, KARNA AUR", "DURYODHANA SAHIT..."], [(35.66, 36.70), (36.70, 37.80)],),
            (37.80, 40.10, ["SAAT MAHARATHIYON NE", "MILKAR..."], [(37.80, 38.90), (38.90, 40.10)]),
            (40.10, 42.30, ["WARFARE KA HAR", "NIYAM TOD KAR..."], [(40.10, 41.20), (41.20, 42.30)]),
            (42.30, 44.46, ["US NIHATTHE BACHHE KO", "GHER LIYA!"], [(42.30, 43.30), (43.30, 44.46)]),
            (44.46, 46.54, ["KYA YE KAURAVON KI", "JEET THI?"], [(44.46, 45.50), (45.50, 46.54)]),
            (46.54, 49.30, ["YA UNKA SABSE BADA", "MORAL DOWNFALL?"], [(46.54, 47.90), (47.90, 49.30)]),
            (49.30, 50.99, ["COMMENT MEIN", "LIKHEIN!"], [(49.30, 50.10), (50.10, 50.99)])
        ]
    elif "chanakya" in audio_basename.lower() or "vishkanya" in audio_basename.lower():
        scenes_meta = [
            {"start": 0.00,  "end": 8.80,  "asset": "alexander",   "zoom": (1.00, 1.15), "pan": (0.50, 0.45), "vfx": "godrays"},
            {"start": 8.80,  "end": 20.04, "asset": "mastermind",  "zoom": (1.05, 1.25), "pan": (0.50, 0.40), "vfx": "particles"},
            {"start": 20.04, "end": 34.80, "asset": "vishkanya",   "zoom": (1.00, 1.18), "pan": (0.50, 0.48), "vfx": "golden_aura"},
            {"start": 34.80, "end": 44.52, "asset": "mutiny",      "zoom": (1.05, 1.22), "pan": (0.50, 0.42), "vfx": "mist"},
            {"start": 44.52, "end": max(duration, 50.0), "asset": "victory", "zoom": (1.10, 1.25), "pan": (0.50, 0.42), "vfx": "golden_aura"},
        ]
        captions = [
            (0.00, 3.64, ["ALEXANDER KI", "GREEK ARMY KO..."], [(0.00, 1.80), (1.80, 3.64)]),
            (3.64, 6.18, ["KISI TALWAR NE NAHI..."], [(3.64, 6.18)]),
            (6.18, 8.80, ["BALKI CHANAKYA KE", "FEAR TRAP NE ROKA!"], [(6.18, 7.50), (7.50, 8.80)]),
            (8.80, 13.22, ["GREEK GENERALS JAB", "MAGADHA BADH RAHE THE"], [(8.80, 11.00), (11.00, 13.22)]),
            (13.22, 16.48, ["CHANAKYA KE PAAS", "5X CHHOTI ARMY THI!"], [(13.22, 14.80), (14.80, 16.48)]),
            (16.48, 20.04, ["UNHONE CHUNA", "ASYMMETRIC WARFARE!"], [(16.48, 18.20), (18.20, 20.04)]),
            (20.04, 22.94, ["RECRUIT KIYA", "VISHKANYAS KO!"], [(20.04, 21.50), (21.50, 22.94)]),
            (22.94, 25.58, ["LETHAL FEMALE SPIES", "POISON NETWORK"], [(22.94, 24.20), (24.20, 25.58)]),
            (25.58, 29.72, ["MICRO-DOSES SE", "IMMUNE & DEADLY!"], [(25.58, 27.60), (27.60, 29.72)]),
            (29.72, 31.90, ["EK POISONED MEAL", "AUR GENERALS..."], [(29.72, 30.80), (30.80, 31.90)]),
            (31.90, 34.80, ["RAATON-RAAT", "KHATAM HO GAYE!"], [(31.90, 33.30), (33.30, 34.80)]),
            (34.80, 38.90, ["GREEK CAMPS MEIN", "AFWAAH FAILI KI..."], [(34.80, 36.80), (36.80, 38.90)]),
            (38.90, 41.24, ["BHARAT MEIN AATE HI", "SHRAPIT HOKAR MARENGE!"], [(38.90, 40.00), (40.00, 41.24)]),
            (41.24, 44.52, ["GREEK SOLDIERS NE", "INSAAR KAR DIYA!"], [(41.24, 42.80), (42.80, 44.52)]),
            (44.52, 47.34, ["BRUTE FORCE YA", "MASTERMIND INTELLIGENCE?"], [(44.52, 45.90), (45.90, 47.34)]),
            (47.34, 49.63, ["COMMENT KAREIN!", "@VIBEITIHAAS"], [(47.34, 48.50), (48.50, 49.63)]),
        ]
    elif "vembu" in audio_basename.lower() or "zoho" in audio_basename.lower() or "shridhar" in audio_basename.lower():
        scenes_meta = [
            {"start": 0.00,  "end": 8.76,  "asset": "silicon_valley", "zoom": (1.00, 1.16), "pan": (0.50, 0.45), "vfx": "particles"},
            {"start": 8.76,  "end": 17.18, "asset": "journey",        "zoom": (1.00, 1.18), "pan": (0.50, 0.42), "vfx": "godrays"},
            {"start": 17.18, "end": 27.66, "asset": "village_hq",     "zoom": (1.05, 1.22), "pan": (0.50, 0.48), "vfx": "particles"},
            {"start": 27.66, "end": 36.60, "asset": "rural_coders",   "zoom": (1.00, 1.18), "pan": (0.50, 0.45), "vfx": "golden_aura"},
            {"start": 36.60, "end": 48.62, "asset": "global_tech",    "zoom": (1.05, 1.25), "pan": (0.50, 0.40), "vfx": "particles"},
            {"start": 48.62, "end": 56.56, "asset": "bicycle",        "zoom": (1.00, 1.18), "pan": (0.50, 0.45), "vfx": "godrays"},
            {"start": 56.56, "end": max(duration, 64.0), "asset": "bicycle", "zoom": (1.18, 1.30), "pan": (0.50, 0.42), "vfx": "golden_aura"},
        ]
        captions = [
            (0.00, 2.18, ["SILICON VALLEY KE", "TOP INVESTORS NE..."], [(0.00, 1.02), (1.02, 2.18)]),
            (2.18, 4.04, ["BILLIONS OF DOLLARS", "OFFER KIYE!"], [(2.18, 3.40), (3.40, 4.04)]),
            (4.04, 6.56, ["LEKIN IS INDIAN", "FOUNDER NE..."], [(4.04, 5.32), (5.32, 6.56)]),
            (6.56, 8.76, ["UNKE CHEQUES UNKE MUNH", "PAR WAPAS FEK DIYE!"], [(6.56, 7.34), (7.34, 8.76)]),
            (8.76, 10.92, ["YE HAIN", "SRIDHAR VEMBU!"], [(8.76, 9.88), (9.88, 10.92)]),
            (10.92, 12.42, ["ZOHO KE", "FOUNDER!"], [(10.92, 11.68), (11.68, 12.42)]),
            (12.42, 15.00, ["JAB SAARI STARTUPS", "HAZARON CRORE KE..."], [(12.42, 13.92), (13.92, 15.00)]),
            (15.00, 17.18, ["FUNDING BURNS AUR", "LAYOFFS MEIN DOOB RAHI THI!"], [(15.00, 15.94), (15.94, 17.18)]),
            (17.18, 19.26, ["SRIDHAR NE", "CALIFORNIA CHHOD KAR..."], [(17.18, 18.04), (18.04, 19.26)]),
            (19.26, 21.98, ["TAMIL NADU KE EK", "CHHOTE SE GAON MEIN..."], [(19.26, 20.38), (20.38, 21.98)]),
            (21.98, 23.56, ["APNA GLOBAL", "HEADQUARTERS KHOL DIYA!"], [(21.98, 22.72), (22.72, 23.56)]),
            (23.56, 25.84, ["NA KOI VC", "FUNDING LI..."], [(23.56, 24.64), (24.64, 25.84)]),
            (25.84, 27.66, ["NA EK RUPAYE", "KA KARZ!"], [(25.84, 26.80), (26.80, 27.66)]),
            (27.66, 30.62, ["BALKI UN GAON KE", "BACHHON KO CODE SIKHAYA..."], [(27.66, 28.88), (28.88, 30.62)]),
            (30.62, 32.92, ["JINHE COLLEGE TAK", "NASEEB NAHI HUA THA!"], [(30.62, 31.80), (31.80, 32.92)]),
            (32.92, 36.60, ["AAJ WAHI GAON KE BACHHE", "AISI CODING KARTE HAIN..."], [(32.92, 34.72), (34.72, 36.60)]),
            (36.60, 40.62, ["GOOGLE, SALESFORCE & MICROSOFT", "BHI DEKH KAR HAIRAN HAIN!"], [(36.60, 38.54), (38.54, 40.62)]),
            (40.62, 43.16, ["ZOHO AAJ 150", "DESHON MEIN..."], [(40.62, 41.74), (41.74, 43.16)]),
            (43.16, 45.54, ["100 MILLION USERS", "SERVE KARTA HAI!"], [(43.16, 44.28), (44.28, 45.54)]),
            (45.54, 48.62, ["AUR HAZARON CRORE KA", "PURE PROFIT BANATA HAI!"], [(45.54, 46.92), (46.92, 48.62)]),
            (48.62, 52.58, ["AUR ITNI BADI", "GLOBAL EMPIRE KE BAAD BHI..."], [(48.62, 50.66), (50.66, 52.58)]),
            (52.58, 54.86, ["GAON MEIN SADHARAN", "DHOTI PEHANTE HAIN..."], [(52.58, 53.90), (53.90, 54.86)]),
            (54.86, 56.56, ["AUR CYCLE PAR", "GHOOMTE HAIN!"], [(54.86, 55.72), (55.72, 56.56)]),
            (56.56, 58.28, ["WESTERN VALUATION", "HYPE?"], [(56.56, 57.40), (57.40, 58.28)]),
            (58.28, 60.60, ["YA ASLI DESI", "SWADESHI PROFIT?"], [(58.28, 59.72), (59.72, 60.60)]),
            (60.60, 61.86, ["COMMENT MEIN", "LIKHEIN:"], [(60.60, 61.42), (61.42, 61.86)]),
            (61.86, 63.24, ["PROUD INDIAN!", "🇮🇳 @VIBEITIHAAS"], [(61.86, 62.50), (62.50, 63.24)])
        ]
    else:
        scenes_meta = [
            {"start": 0.00,  "end": 3.70,  "asset": "everest",      "zoom": (1.0, 1.10),  "pan": (0.50, 0.48), "vfx": "godrays"},
            {"start": 3.70,  "end": 8.62,  "asset": "kailash_day",  "zoom": (1.0, 1.12),  "pan": (0.50, 0.52), "vfx": "particles"},
            {"start": 8.62,  "end": 14.50, "asset": "kailash_day",  "zoom": (1.15, 1.28), "pan": (0.50, 0.38), "vfx": "godrays"},
            {"start": 14.50, "end": 19.60, "asset": "axis_night",   "zoom": (1.0, 1.15),  "pan": (0.50, 0.50), "vfx": "particles"},
            {"start": 19.60, "end": 25.78, "asset": "everest",      "zoom": (1.12, 1.22), "pan": (0.46, 0.55), "vfx": "mist"},
            {"start": 25.78, "end": 32.22, "asset": "axis_night",   "zoom": (1.10, 1.22), "pan": (0.50, 0.45), "vfx": "particles"},
            {"start": 32.22, "end": 37.34, "asset": "axis_night",   "zoom": (1.22, 1.35), "pan": (0.50, 0.40), "vfx": "particles"},
            {"start": 37.34, "end": 40.68, "asset": "kailash_day",  "zoom": (1.20, 1.30), "pan": (0.45, 0.48), "vfx": "particles"},
            {"start": 40.68, "end": 45.06, "asset": "everest",      "zoom": (1.05, 1.18), "pan": (0.50, 0.46), "vfx": "blizzard"},
            {"start": 45.06, "end": 50.66, "asset": "axis_night",   "zoom": (1.15, 1.05), "pan": (0.50, 0.52), "vfx": "mist"},
            {"start": 50.66, "end": 56.38, "asset": "kailash_day",  "zoom": (1.0, 1.12),  "pan": (0.42, 0.65), "vfx": "godrays"},
            {"start": 56.38, "end": 61.92, "asset": "axis_night",   "zoom": (1.08, 1.18), "pan": (0.55, 0.60), "vfx": "mist"},
            {"start": 61.92, "end": 67.88, "asset": "kailash_day",  "zoom": (1.10, 1.25), "pan": (0.50, 0.42), "vfx": "golden_aura"},
            {"start": 67.88, "end": max(duration, 73.0), "asset": "axis_night", "zoom": (1.15, 1.30), "pan": (0.50, 0.42), "vfx": "golden_aura"},
        ]

        # Kinetic Subtitles
        captions = [
            (0.00, 1.45, ["MOUNT", "EVEREST"], [(0.00, 0.60), (0.60, 1.45)]),
            (1.45, 3.20, ["7000+ LOG", "CHADH CHUKE"], [(1.45, 2.30), (2.30, 3.20)]),
            (3.70, 5.00, ["2000M CHHOTE", "KAILASH"], [(3.70, 4.40), (4.40, 5.00)]),
            (5.00, 6.26, ["PARVAT", "PAR..."], [(5.00, 5.60), (5.60, 6.26)]),
            (6.26, 7.50, ["AAJ TAK KOI", "INSAAN"], [(6.26, 6.90), (6.90, 7.50)]),
            (7.50, 8.62, ["KYUN NAHI", "CHADH PAYA?"], [(7.50, 8.00), (8.00, 8.62)]),
            (9.90, 11.58, ["SCIENTISTS KE", "ANUSAAR"], [(9.90, 10.70), (10.70, 11.58)]),
            (11.58, 13.20, ["KAILASH", "PARVAT"], [(11.58, 12.40), (12.40, 13.20)]),
            (13.20, 14.50, ["SIRF EK", "PAHAD NAHI"], [(13.20, 13.80), (13.80, 14.50)]),
            (14.50, 16.50, ["POORI PRITHVI KA", "KENDRA"], [(14.50, 15.60), (15.60, 16.50)]),
            (16.50, 18.84, ["YAANI", "AXIS MUNDI!"], [(16.50, 17.50), (17.50, 18.84)]),
            (19.60, 21.14, ["1999 MEIN", "EXPEDITION"], [(19.60, 20.30), (20.30, 21.14)]),
            (21.14, 23.36, ["RUSSIAN", "MOUNTAINEERS"], [(21.14, 22.20), (22.20, 23.36)]),
            (23.36, 25.22, ["CHADHNE KI", "KOSHISH KI"], [(23.36, 24.20), (24.20, 25.22)]),
            (25.78, 27.78, ["KHAUFNAK", "RAAZ DEKHA!"], [(25.78, 26.70), (26.70, 27.78)]),
            (28.38, 29.80, ["PARVAT KE PAAS", "JAATE HI"], [(28.38, 29.10), (29.10, 29.80)]),
            (29.80, 31.70, ["WAQT KI RAFTAAR", "2X DUGNI!"], [(29.80, 30.70), (30.70, 31.70)]),
            (32.22, 33.80, ["SIRF 12", "GHANTE MEIN"], [(32.22, 33.00), (33.00, 33.80)]),
            (33.80, 35.20, ["BAAL AUR", "NAKHUN"], [(33.80, 34.50), (34.50, 35.20)]),
            (35.20, 36.76, ["KAI DINO JITNE", "BADH GAYE!"], [(35.20, 36.00), (36.00, 36.76)]),
            (37.34, 39.22, ["COMPASS", "GHOOMNE LAGA!"], [(37.34, 38.30), (38.30, 39.22)]),
            (39.22, 40.68, ["JO BHI", "AAGE BADHA"], [(39.22, 39.90), (39.90, 40.68)]),
            (40.68, 42.20, ["ACHANAK AAYE", "BARFEELE"], [(40.68, 41.50), (41.50, 42.20)]),
            (42.20, 44.32, ["TOOFANO NE", "PEECHE DHAKELA!"], [(42.20, 43.20), (43.20, 44.32)]),
            (45.06, 47.06, ["KUCH HI HAFTON", "MEIN"], [(45.06, 46.10), (46.10, 47.06)]),
            (47.06, 50.06, ["AJEEB BIMAARI SE", "CHAL BASE..."], [(47.06, 48.50), (48.50, 50.06)]),
            (50.66, 53.08, ["2 ANOKHI", "JHEELEIN"], [(50.66, 51.90), (51.90, 53.08)]),
            (53.08, 54.80, ["LAKE", "MANSAROVAR"], [(53.08, 53.90), (53.90, 54.80)]),
            (54.80, 56.38, ["AMRIT JAISA", "SHAANT PAANI"], [(54.80, 55.60), (55.60, 56.38)]),
            (56.38, 58.00, ["AUR LAKE", "RAKSHASTAL"], [(56.38, 57.20), (57.20, 58.00)]),
            (58.00, 59.50, ["KHAARA PAANI", "SALT WATER"], [(58.00, 58.80), (58.80, 59.50)]),
            (59.50, 61.00, ["AAJ BHI", "ASHAANT HAI!"], [(59.50, 60.20), (60.20, 61.00)]),
            (61.92, 63.50, ["KAHA JAATA HAI", "MYSTERY"], [(61.92, 62.70), (62.70, 63.50)]),
            (63.50, 65.20, ["KAILASH", "PARVAT PAR"], [(63.50, 64.30), (64.30, 65.20)]),
            (65.20, 67.88, ["KEWAL SIDDH", "AATMAAYEIN!"], [(65.20, 66.50), (66.50, 67.88)]),
            (67.88, 69.10, ["COMMENT MEIN"], [(67.88, 69.10)]),
            (69.10, 70.44, ["HAR HAR MAHADEV!"], [(69.10, 70.44)]),
            (70.44, 71.70, ["FOLLOW"], [(70.44, 71.70)]),
            (71.70, 72.98, ["@VIBEITIHAAS"], [(71.70, 72.98)])
        ]

    # Pre-generate particles
    random.seed(108)
    particles = []
    for _ in range(65):
        particles.append({
            'x': random.uniform(50, W - 50),
            'y': random.uniform(100, H - 200),
            'r': random.uniform(3, 7.5),
            'speed_y': random.uniform(25, 60),
            'wobble_freq': random.uniform(1.2, 2.6),
            'wobble_amp': random.uniform(15, 35),
            'phase': random.uniform(0, math.pi * 2),
            'color': random.choice([(255, 235, 120), (255, 215, 0), (180, 240, 255), (255, 255, 255)])
        })

    blizzard_particles = []
    for _ in range(130):
        blizzard_particles.append({
            'x': random.uniform(-100, W + 100),
            'y': random.uniform(-100, H + 100),
            'length': random.uniform(22, 55),
            'speed_x': random.uniform(750, 1250),
            'speed_y': random.uniform(550, 950),
            'width': random.choice([2, 3, 4]),
            'alpha': random.randint(130, 240)
        })

    # Prepare Brand Badge (Checks root directory logo.png first, safe from assets clearing)
    brand_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_brand = ImageDraw.Draw(brand_overlay)
    for y in range(220):
        a = int(160 * (1.0 - y / 220.0))
        d_brand.line([(0, y), (W, y)], fill=(8, 12, 18, a))
    for y in range(H - 420, H):
        a = int(210 * ((y - (H - 420)) / 420.0))
        d_brand.line([(0, y), (W, y)], fill=(8, 12, 18, a))

    # Look for logo.png in project root (protected from asset deletion)
    logo_path = os.path.join(SCRIPT_DIR, "logo.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(ASSETS_DIR, "logo.png")

    has_logo = os.path.exists(logo_path)
    font_brand = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)

    if has_logo:
        logo_raw = Image.open(logo_path).convert('RGBA')
        logo_size = 64
        logo = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        mask = Image.new('L', (logo_size, logo_size), 0)
        d_mask = ImageDraw.Draw(mask)
        d_mask.ellipse((0, 0, logo_size, logo_size), fill=255)

        pill_w = 285
        pill_h = 76
        pill_x = 50
        pill_y = 60
        d_brand.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                                 radius=38, fill=(10, 16, 26, 225), outline=(255, 215, 0, 230), width=2)
        brand_overlay.paste(logo, (pill_x + 6, pill_y + 6), mask)
        d_brand.text((pill_x + 82, pill_y + 20), "vibeitihaas", fill=(255, 255, 255, 255), font=font_brand)
    else:
        # Fallback text badge if logo.png is ever missing
        pill_w = 230
        pill_h = 66
        pill_x = 50
        pill_y = 65
        d_brand.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                                 radius=33, fill=(10, 16, 26, 225), outline=(255, 215, 0, 230), width=2)
        d_brand.text((pill_x + 28, pill_y + 16), "@vibeitihaas", fill=(255, 255, 255, 255), font=font_brand)

    print("Clean brand badge prepared (vibeitihaas).")

    def render_frame(f):
        current_time = f / FPS
        active_scene = scenes_meta[-1]
        for sc in scenes_meta:
            if sc["start"] <= current_time <= sc["end"]:
                active_scene = sc
                break

        sc_dur = max(0.01, active_scene["end"] - active_scene["start"])
        t = min(1.0, max(0.0, (current_time - active_scene["start"]) / sc_dur))

        z_start, z_end = active_scene["zoom"]
        zoom = z_start + (z_end - z_start) * t

        base_img = assets[active_scene["asset"]]
        bw, bh = base_img.size
        cw = int(W / zoom)
        ch = int(H / zoom)
        px, py = active_scene["pan"]
        cx = int(bw * px)
        cy = int(bh * py)
        x1 = max(0, min(bw - cw, cx - cw // 2))
        y1 = max(0, min(bh - ch, cy - ch // 2))
        x2 = x1 + cw
        y2 = y1 + ch

        crop = base_img.crop((x1, y1, x2, y2))
        frame = crop.resize((W, H), Image.Resampling.BILINEAR).convert('RGBA')

        # Dynamic VFX Layer
        vfx_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d_vfx = ImageDraw.Draw(vfx_overlay)
        vfx_type = active_scene["vfx"]

        if vfx_type in ("godrays", "golden_aura"):
            ray_pulse = 0.17 + 0.08 * math.sin(current_time * 2.0)
            alpha = int(255 * ray_pulse)
            ray_color = (255, 235, 160, alpha)
            rays = [
                [(160, 0), (360, 0), (W + 200, H), (W - 100, H)],
                [(460, 0), (630, 0), (W + 400, H), (W + 150, H)],
                [(-80, 100), (20, 0), (W - 220, H), (W - 420, H)]
            ]
            for r in rays:
                d_vfx.polygon(r, fill=ray_color)

        if vfx_type in ("particles", "godrays", "golden_aura", "mist"):
            for p in particles:
                py_pos = (p['y'] - current_time * p['speed_y']) % H
                px_pos = p['x'] + math.sin(current_time * p['wobble_freq'] + p['phase']) * p['wobble_amp']
                alpha = int(170 + 70 * math.sin(current_time * 3.5 + p['phase']))
                r = p['r']
                d_vfx.ellipse([px_pos - r, py_pos - r, px_pos + r, py_pos + r], fill=(*p['color'], alpha))
                d_vfx.ellipse([px_pos - r*2.2, py_pos - r*2.2, px_pos + r*2.2, py_pos + r*2.2], fill=(*p['color'], int(alpha * 0.35)))

        if vfx_type == "golden_aura":
            ring_r = int(130 + 90 * math.sin(current_time * 3.0))
            d_vfx.ellipse([W//2 - ring_r, H//2 - ring_r - 180, W//2 + ring_r, H//2 + ring_r - 180],
                         outline=(255, 220, 100, 130), width=6)

        frame = Image.alpha_composite(frame, vfx_overlay)
        frame = Image.alpha_composite(frame, brand_overlay)

        # Progress bar
        d_out = ImageDraw.Draw(frame)
        pad_b = 50
        bar_y = H - pad_b - 20
        d_out.line([(pad_b, bar_y), (W - pad_b, bar_y)], fill=(60, 70, 85, 180), width=6)
        prog_pct = min(1.0, current_time / duration)
        prog_w = int((W - 2 * pad_b) * prog_pct)
        d_out.line([(pad_b, bar_y), (pad_b + prog_w, bar_y)], fill=(255, 215, 0), width=6)

        # Safe kinetic subtitles
        for cap in captions:
            c_start, c_end, words, timings = cap
            if c_start <= current_time <= c_end:
                active_idx = 0
                for wi, (ws, we) in enumerate(timings):
                    if ws <= current_time <= we:
                        active_idx = wi
                        break

                base_font_size = 78
                font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Impact.ttf', base_font_size)
                space_w = int(base_font_size * 0.32)
                boxes = [d_out.textbbox((0, 0), w, font=font) for w in words]
                widths = [b[2] - b[0] for b in boxes]
                total_w = sum(widths) + space_w * (len(words) - 1)

                if total_w > MAX_SAFE_W:
                    font_size = max(46, int(base_font_size * (MAX_SAFE_W / total_w)))
                    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Impact.ttf', font_size)
                    space_w = int(font_size * 0.32)
                    boxes = [d_out.textbbox((0, 0), w, font=font) for w in words]
                    widths = [b[2] - b[0] for b in boxes]
                    total_w = sum(widths) + space_w * (len(words) - 1)
                else:
                    font_size = base_font_size

                start_x = (W - total_w) // 2
                y_base = 1200
                curr_x = start_x

                for wi, w in enumerate(words):
                    is_active = (wi == active_idx)
                    wb = boxes[wi]
                    if is_active:
                        fill_col = (255, 230, 0)
                        stroke_col = (10, 15, 20)
                        stroke_w = max(6, int(font_size * 0.12))
                        pad_x = int(font_size * 0.22)
                        pad_y = int(font_size * 0.12)
                        d_out.rounded_rectangle([curr_x - pad_x, y_base + wb[1] - pad_y,
                                                curr_x + widths[wi] + pad_x, y_base + wb[3] + pad_y],
                                                radius=14, fill=(15, 20, 30, 230), outline=(255, 215, 0), width=3)
                    else:
                        fill_col = (255, 255, 255)
                        stroke_col = (10, 15, 20)
                        stroke_w = max(5, int(font_size * 0.09))

                    d_out.text((curr_x, y_base), w, font=font, fill=fill_col, stroke_fill=stroke_col, stroke_width=stroke_w)
                    curr_x += widths[wi] + space_w
                break

        return frame.convert('RGB').tobytes()

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_file,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_file
    ]

    print("Encoding video short via FFmpeg...")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    start_time = time.time()
    for f in range(total_frames):
        raw_bytes = render_frame(f)
        proc.stdin.write(raw_bytes)
        if f % 150 == 0 or f == total_frames - 1:
            fps_so_far = (f + 1) / max(0.01, time.time() - start_time)
            pct = ((f + 1) / total_frames) * 100
            print(f"Progress: {f+1}/{total_frames} ({pct:.1f}%) | {fps_so_far:.1f} FPS")

    proc.stdin.close()
    proc.wait()

    elapsed = time.time() - start_time
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print("=======================================================")
    print(f"SUCCESS: Render completed in {elapsed:.1f}s!")
    print(f"Final Video: {output_file} ({size_mb:.2f} MB)")
    print("=======================================================")

    # Automatically generate companion viral metadata package (.txt)
    meta_txt_file = os.path.join(OUTPUT_DIR, f"{audio_basename}_metadata.txt")
    generate_metadata_package(audio_basename, transcript, meta_txt_file)
    print(f"Viral Metadata Generated: {meta_txt_file}")
    print("=======================================================")

if __name__ == '__main__':
    main()
