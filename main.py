import os
import sys
import time
import subprocess
import platform
import re
import array
import shutil
import urllib.request
import zipfile

def check_and_install_requirements():
    """Gerekli araçları ve kütüphaneleri kontrol eder ve yükler."""
    print("="*60)
    print("🔍 Sistem Gereksinimleri Kontrol Ediliyor...")
    print("="*60 + "\n")
    
    # Python kütüphanelerini kontrol et
    required_packages = {
        'yt_dlp': 'yt-dlp',
        'pydub': 'pydub',
        'pygame': 'pygame',
        'requests': 'requests',
        'scipy': 'scipy',
        'numpy': 'numpy'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {pip_name} yüklü")
        except ImportError:
            print(f"❌ {pip_name} bulunamadı")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n📦 Eksik paketler yükleniyor: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Tüm Python paketleri yüklendi!\n")
        except subprocess.CalledProcessError:
            print("❌ Paket yükleme hatası! Manuel olarak yükleyin:")
            print(f"   pip install {' '.join(missing_packages)}")
            sys.exit(1)
    
    # FFmpeg kontrolü
    if not check_ffmpeg():
        print("\n❌ FFmpeg bulunamadı!")
        if platform.system() == "Windows":
            install_ffmpeg_windows()
        else:
            print("FFmpeg'i manuel olarak yükleyin:")
            print("  Linux: sudo apt install ffmpeg")
            print("  macOS: brew install ffmpeg")
            sys.exit(1)
    else:
        print("✅ FFmpeg yüklü")
    
    print("\n" + "="*60)
    print("✅ Tüm gereksinimler hazır!")
    print("="*60 + "\n")
    time.sleep(1)

def check_ffmpeg():
    """FFmpeg'in yüklü olup olmadığını kontrol eder."""
    return shutil.which("ffmpeg") is not None

def install_ffmpeg_windows():
    """Windows için FFmpeg'i otomatik indirir ve kurar."""
    print("\n📥 FFmpeg indiriliyor (Windows)...")
    
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    ffmpeg_zip = "ffmpeg.zip"
    ffmpeg_dir = "ffmpeg"
    
    try:
        # İndir
        print("⬇️ İndiriliyor... (Bu biraz zaman alabilir)")
        urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
        
        # Aç
        print("📂 Dosyalar çıkarılıyor...")
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        
        # ffmpeg.exe'yi bul ve PATH'e ekle
        for root, dirs, files in os.walk(ffmpeg_dir):
            if "ffmpeg.exe" in files:
                ffmpeg_path = root
                
                # Mevcut dizine kopyala
                shutil.copy(os.path.join(ffmpeg_path, "ffmpeg.exe"), "ffmpeg.exe")
                print("✅ FFmpeg başarıyla yüklendi!")
                
                # Temizlik
                os.remove(ffmpeg_zip)
                shutil.rmtree(ffmpeg_dir)
                return
        
        print("❌ FFmpeg kurulumu başarısız!")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ FFmpeg indirme hatası: {e}")
        print("\nManuel kurulum:")
        print("1. https://ffmpeg.org/download.html adresine gidin")
        print("2. Windows sürümünü indirin")
        print("3. ffmpeg.exe'yi bu programın dizinine koyun")
        sys.exit(1)

# Gereksinimleri kontrol et
check_and_install_requirements()


import yt_dlp
import requests
from pydub import AudioSegment
from pydub.scipy_effects import low_pass_filter
import pygame

def clean_filename(title):
    """Dosya adındaki yasaklı karakterleri temizler."""
    # Windows için özel karakter filtresi
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '')
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).rstrip()

def download_from_youtube(youtube_url):
    print(f"⬇️ Video indiriliyor...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'temp_song.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            video_title = info.get('title', 'Unknown Song')
            video_artist = info.get('artist', '')
            
            # Windows'ta temp_song.mp3 olarak kaydedilir
            return "temp_song.mp3", video_title, video_artist
    except Exception as e:
        print(f"❌ İndirme Hatası: {e}")
        return None, None, None

def make_it_bass_boosted(file_path, bass_level=12, distortion_level=8):

    print("🔊 Bass & Distortion uygulanıyor...")

    sound = AudioSegment.from_mp3(file_path)


    distorted = sound + distortion_level

    samples = distorted.get_array_of_samples()
    sample_type = samples.typecode

    clipped = array.array(sample_type, samples)

    max_val = max(abs(x) for x in clipped)
    threshold = int(max_val * 0.75)

    for i in range(len(clipped)):
        if clipped[i] > threshold:
            clipped[i] = threshold
        elif clipped[i] < -threshold:
            clipped[i] = -threshold

    clipped_bytes = clipped.tobytes()
    distorted = distorted._spawn(clipped_bytes)


    bass_line = low_pass_filter(distorted, 150)
    bass_line = bass_line + bass_level

    final_sound = (distorted - 2).overlay(bass_line)
    loud_sound = final_sound + 3

    output_path = "boosted_song.mp3"
    loud_sound.export(output_path, format="mp3")

    return output_path

def search_lyrics(search_term):

    try:
        url = f"https://lrclib.net/api/search?q={search_term.replace(' ', '+')}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                synced_lyrics = results[0].get('syncedLyrics', '')
                if synced_lyrics:
                    return synced_lyrics
    except Exception as e:
        print(f"⚠️ Şarkı sözü arama hatası: {e}")
    
    return None

def parse_lrc(lrc_string):

    lyrics_data = []
    if not lrc_string:
        return []
    
    pattern = re.compile(r'\[(\d+):(\d+\.\d+)\](.*)')
    
    for line in lrc_string.split('\n'):
        match = pattern.match(line)
        if match:
            minutes = int(match.group(1))
            seconds = float(match.group(2))
            text = match.group(3).strip()
            if text:  # Boş satırları atla
                total_seconds = (minutes * 60) + seconds
                lyrics_data.append({'time': total_seconds, 'text': text})
            
    return lyrics_data

def create_srt_file(lyrics_data, output_file="lyrics.srt"):

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, lyric in enumerate(lyrics_data):
            start_time = lyric['time']
            
            if i < len(lyrics_data) - 1:
                end_time = lyrics_data[i + 1]['time']
            else:
                end_time = start_time + 3.0
            
            f.write(f"{i + 1}\n")
            f.write(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}\n")
            f.write(f"{lyric['text']}\n\n")
    
    return output_file

def format_srt_time(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_visualizer_video(audio_file, output_file="visualizer_temp.mp4"):

    print("🎨 Techno Visualizer oluşturuluyor...")
    
    try:
        ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
        

        video_filter = (

            "[0:a]showwaves=s=1280x720:mode=cline:rate=25:colors=0xff00ff|0x00ffff|0xff0080:scale=sqrt[waves];"
            

            "[0:a]showfreqs=s=1280x400:mode=bar:ascale=log:fscale=log:"
            "colors=0xff00ff|0x00ffff|0xffff00|0xff0080[freq];"
            

            "[waves][freq]overlay=0:160:format=auto[combined];"
            

            "[combined]eq=contrast=1.4:brightness=0.05:saturation=1.8:gamma=1.1,"
            "hue=h=t*30:s=1.5,"  
            "unsharp=5:5:1.5:5:5:0"  
        )
        
        cmd = [
            ffmpeg_cmd,
            '-i', audio_file,
            '-filter_complex', video_filter,
            '-pix_fmt', 'yuv420p',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'copy',
            '-shortest',
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Visualizer oluşturuldu!")
            return output_file
        else:
            print(f"⚠️ Visualizer oluşturulamadı, fallback kullanılacak...")
            return None
        
    except Exception as e:
        print(f"⚠️ Visualizer hatası: {e}")
        return None

def create_video_with_lyrics(audio_file, lyrics_data, title, output_file):
    """Techno visualizer + neon şarkı sözleriyle video oluşturur - Linux uyumlu."""
    print("🎬 Techno MP4 video oluşturuluyor...")
    
    # Önce visualizer'ı oluştur
    visualizer_file = create_visualizer_video(audio_file)
    
    if not visualizer_file or not os.path.exists(visualizer_file):
        print("📹 Direkt altyazılı video oluşturuluyor...")
        visualizer_file = None
    
    srt_file = create_srt_file(lyrics_data)
    srt_file_escaped = srt_file.replace('\\', '/').replace(':', '\\:')
    
    try:
        ffmpeg_cmd = "ffmpeg.exe" if os.path.exists("ffmpeg.exe") else "ffmpeg"
        
        if visualizer_file:
            cmd = [
                ffmpeg_cmd,
                '-i', visualizer_file,
                '-vf', (
                    f"subtitles={srt_file_escaped}:"
                    "force_style='FontName=Impact,FontSize=48,Bold=1,"
                    "PrimaryColour=&H00FFFF,OutlineColour=&HFF00FF,"
                    "BorderStyle=1,Outline=4,Shadow=3,"
                    "Alignment=5,MarginV=50'"
                ),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'copy',
                '-y',
                output_file
            ]
        else:
            cmd = [
                ffmpeg_cmd,
                '-i', audio_file,
                '-filter_complex',
                (
                    # background
                    "[0:a]showwaves=s=1280x720:mode=cline:rate=25:"
                    "colors=0xff00ff|0x00ffff|0xff0080:scale=sqrt[waves];"
                    
                    # Frequency bars
                    "[0:a]showfreqs=s=1280x400:mode=bar:ascale=log:fscale=log:"
                    "colors=0xff00ff|0x00ffff|0xffff00[freq];"
                    
                    # Combine
                    "[waves][freq]overlay=0:160:format=auto[bg];"
                    
                    # Color
                    "[bg]eq=contrast=1.4:saturation=1.8:gamma=1.1,"
                    "hue=h=t*30:s=1.5,"
                    
                    # neon lyrics
                    f"subtitles={srt_file_escaped}:"
                    "force_style='FontName=Impact,FontSize=48,Bold=1,"
                    "PrimaryColour=&H00FFFF,OutlineColour=&HFF00FF,"
                    "BorderStyle=1,Outline=4,Shadow=3,"
                    "Alignment=5,MarginV=50'"
                ),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-preset', 'medium',
                '-crf', '23',
                '-shortest',
                '-y',
                output_file
            ]
        
        print("⏳ Video render ediliyor...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video kaydedildi: {output_file}")
        else:
            print(f"❌ Video oluşturma hatası!")
            stderr_lines = result.stderr.split('\n')
            for line in stderr_lines[-20:]:  # Son 20 satır
                if 'error' in line.lower() or 'invalid' in line.lower():
                    print(f"  → {line.strip()}")
        
        # Temizlik
        if visualizer_file and os.path.exists(visualizer_file):
            try:
                os.remove(visualizer_file)
            except:
                pass
        
    except FileNotFoundError:
        print("❌ FFmpeg bulunamadı!")
    except Exception as e:
        print(f"❌ Video oluşturma hatası: {e}")
    finally:
        if os.path.exists(srt_file):
            try:
                os.remove(srt_file)
            except:
                pass

def play_with_lyrics(audio_path, lyrics_data, song_title):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        print("\n" + "="*60)
        print(f"🎧 ÇALINIYOR: {song_title}")
        print("="*60 + "\n")

        start_time = time.time()
        lyric_index = 0
        
        while pygame.mixer.music.get_busy():
            current_time = time.time() - start_time
            
            if lyrics_data and lyric_index < len(lyrics_data):
                next_lyric = lyrics_data[lyric_index]
                
                if current_time >= next_lyric['time']:
                    print(f"🎤 {next_lyric['text']}")
                    lyric_index += 1
            
            time.sleep(0.1)
        
        print("\n✅ Çalma tamamlandı!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Durduruldu.")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"❌ Çalma hatası: {e}")
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*60)
    print("🎵 YouTube Bass Boosted Music Player 🎵")
    print("="*60)
    
    url = input("\n🔗 YouTube Linkini Yapıştır: ").strip()
    
    if not url:
        print("❌ Geçersiz URL!")
        input("\nÇıkmak için Enter'a basın...")
        sys.exit()
    
    print("\n📁 Format Seç:")
    print("  1️⃣  MP3 (Sadece Ses)")
    print("  2️⃣  MP4 (Video + Şarkı Sözleri)")
    format_choice = input("\n➡️  Seçiminiz (1/2): ").strip()
    
    save_as_video = (format_choice == "2")
    
    # İndir
    dosya, baslik, sanatci = download_from_youtube(url)
    
    if dosya and os.path.exists(dosya):
        # Sözleri Bul
        print(f"\n📜 '{baslik}' için sözler aranıyor...")
        
        arama_terimi = f"{sanatci} {baslik}" if sanatci else baslik
        lrc_sozler = search_lyrics(arama_terimi)

        if lrc_sozler:
            print("✅ Zamanlı sözler bulundu!")
            parsed_lyrics = parse_lrc(lrc_sozler)
        else:
            print("⚠️ Zamanlı sözler bulunamadı. Sadece müzik kaydedilecek.")
            parsed_lyrics = []

        # Bass Boost Yap
        boosted_file = make_it_bass_boosted(dosya, bass_level=14)
        
        # Kaydet
        clean_title = clean_filename(baslik)
        
        if save_as_video and parsed_lyrics:
            output_video = f"{clean_title}_boosted.mp4"
            create_video_with_lyrics(boosted_file, parsed_lyrics, baslik, output_video)
        else:
            output_audio = f"{clean_title}_boosted.mp3"
            if os.path.exists(output_audio):
                os.remove(output_audio)
            shutil.copy(boosted_file, output_audio)
            print(f"✅ MP3 kaydedildi: {output_audio}")
        
        # Oynat
        print("\n🎵 Şarkı çalınıyor...\n")
        time.sleep(1)
        play_with_lyrics(boosted_file, parsed_lyrics, baslik)
        
        # Temizlik
        try:
            if os.path.exists("temp_song.mp3"):
                os.remove("temp_song.mp3")
            if os.path.exists("boosted_song.mp3"):
                os.remove("boosted_song.mp3")
        except:
            pass
            
        print("\n" + "="*60)
        print("✅ İşlem Tamamlandı!")
        print("="*60)
    else:
        print("❌ İndirme başarısız oldu!")
    
    input("\nÇıkmak için Enter'a basın...")
