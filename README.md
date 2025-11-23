# 🎵 YouTube Bass Boosted Music Player

YouTube'dan müzik indirip **bass boost** uygulayan, **şarkı sözlerini senkronize** eden ve **techno visualizer** ile MP4 video oluşturan Python uygulaması.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Özellikler

- 🎧 **YouTube İndirme** - Herhangi bir YouTube videosundan ses çıkarma
- 🔊 **Bass Boost & Distortion** - Profesyonel ses efektleri
- 📜 **Otomatik Şarkı Sözü** - Zamanlı şarkı sözlerini otomatik bulma (lrclib.net API)
- 🎬 **Techno Visualizer** - Ritime göre hareketli video oluşturma
- 💾 **Çoklu Format** - MP3 (sadece ses) veya MP4 (görsel + sözler)
- 🎨 **Neon Altyazılar** - Ortada, büyük ve parlak şarkı sözleri
- 🎮 **Canlı Çalma** - Terminal'de senkronize şarkı sözleriyle dinleme
- ⚙️ **Otomatik Kurulum** - İlk çalıştırmada tüm gereksinimleri yükler

## 🎬 Demo
[Lil Zey  DELIKANSIZ_boosted.mp3](https://github.com/user-attachments/files/23695306/Lil.Zey.DELIKANSIZ_boosted.mp3)



### MP4 Çıktısı Özellikleri:
- ✅ Hareketli dalga formları (showwaves)
- ✅ Bass ağırlıklı frekans spektrumu
- ✅ Dönen renk döngüsü
- ✅ Neon efektli altyazılar (cyan + magenta)
- ✅ HD kalite (1280x720)

### Terminal Çıktısı:
```
============================================================
🎧 ÇALINIYOR: Song Name - Artist
============================================================

🎤 First line of lyrics
🎤 Second line of lyrics
🎤 Third line of lyrics...
```

## 🚀 Kurulum

### Gereksinimler

Program ilk çalıştırmada **otomatik olarak** tüm gereksinimleri kontrol eder ve yükler:

- **Python 3.8+**
- **FFmpeg** (otomatik indirilir)
- **Python Paketleri** (otomatik yüklenir):
  - yt-dlp
  - pydub
  - pygame
  - requests
  - scipy
  - numpy

### Hızlı Başlangıç

```bash
# 1. Repoyu klonlayın
https://github.com/yoskasss/YouTube-Bass-Boosted-Music-Player/
cd YouTube-Bass-Boosted-Music-Player

# 2. Çalıştırın (ilk çalıştırma tüm gereksinimleri yükler)
python main.py
```

### Manuel Kurulum (Opsiyonel)

Eğer otomatik kurulum çalışmazsa:

```bash
# Python paketlerini yükle
pip install yt-dlp pydub pygame requests scipy numpy

# FFmpeg'i yükle
# Windows: https://ffmpeg.org/download.html
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

## 📖 Kullanım

```bash
python main.py
```

Program sırayla soracak:

1. **YouTube Linki** - İndirmek istediğiniz videonun URL'si
2. **Format** - MP3 (1) veya MP4 (2)

### Örnek:

```bash
YouTube Linkini Yapıştır: https://www.youtube.com/watch?v=dQw4w9WgXcQ

📁 Format Seç:
  1️⃣  MP3 (Sadece Ses)
  2️⃣  MP4 (Video + Şarkı Sözleri)

➡️  Seçiminiz (1/2): 2
```

Program şunları yapacak:
- ⬇️ YouTube'dan indirir
- 📜 Şarkı sözlerini arar
- 🔊 Bass boost uygular
- 🎬 Video oluşturur (MP4 seçildiyse)
- 💾 Dosyayı kaydeder
- 🎵 Terminal'de çalar

## ⚙️ Bass Boost Ayarları

`make_it_bass_boosted()` fonksiyonundaki parametreleri değiştirerek efekti özelleştirebilirsiniz:

```python
boosted_file = make_it_bass_boosted(
    dosya, 
    bass_level=14,        # Bass seviyesi (0-20)
    distortion_level=8    # Distortion seviyesi (0-15)
)
```

## 🎨 Video Görselleştirme Detayları

### Visualizer Katmanları:
1. **Waveform** - Renkli dalga çizgileri
2. **Frequency Spectrum** - Bass ağırlıklı bar grafikler
3. **Color Rotation** - Sürekli değişen renk döngüsü
4. **Enhancement** - Kontrast, doygunluk, keskinlik

### Altyazı Özellikleri:
- Font: **Impact** (Bold)
- Boyut: **48pt**
- Renk: **Cyan** (ana) + **Magenta** (kontur)
- Konum: **Tam ortada** (Alignment=5)
- Efekt: Gölge + parlama

## 📁 Çıktı Dosyaları

```
SarkiAdi_boosted.mp3   # Sadece MP3 seçilirse
SarkiAdi_boosted.mp4   # MP4 seçilirse (video + ses + sözler)
```

## 🐛 Sorun Giderme

### FFmpeg Bulunamadı
```bash
# Windows
# ffmpeg.exe'yi program klasörüne kopyalayın

# Linux/Ubuntu
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Şarkı Sözü Bulunamadı
- Program otomatik olarak lrclib.net'te arar
- Bulamazsa sadece müzik kaydedilir/çalınır
- Manuel olarak başka kaynaklardan LRC dosyası bulabilirsiniz

### Video Oluşturma Hatası
- FFmpeg'in güncel olduğundan emin olun: `ffmpeg -version`
- Disk alanınızı kontrol edin (en az 500MB boş alan)
- Hata mesajını kontrol edin ve GitHub Issues'a bildirin

## 🔧 Teknik Detaylar

### Ses İşleme:
- **Format**: MP3, 192kbps
- **Bass Boost**: Low-pass filter (150Hz) + overlay
- **Distortion**: Clipping threshold (%75)
- **Normalization**: +3dB final gain

### Video İşleme:
- **Codec**: H.264 (libx264)
- **Preset**: Medium (hız/kalite dengesi)
- **CRF**: 23 (yüksek kalite)
- **Çözünürlük**: 1280x720 (HD)
- **Frame Rate**: 25 FPS

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Yapılacaklar

- [ ] GUI arayüzü (Tkinter/PyQt)
- [ ] Playlist desteği (birden fazla şarkı)
- [ ] Özel visualizer temaları
- [ ] Equalizer ayarları
- [ ] Spotify entegrasyonu
- [ ] Daha fazla şarkı sözü kaynağı

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube indirme
- [pydub](https://github.com/jiaaro/pydub) - Ses işleme
- [pygame](https://www.pygame.org/) - Ses çalma
- [lrclib.net](https://lrclib.net/) - Şarkı sözü API
- [FFmpeg](https://ffmpeg.org/) - Video/ses encoding

## 📧 İletişim

Sorularınız veya önerileriniz için GitHub Issues kullanın.

---

⭐ **Projeyi beğendiyseniz yıldız vermeyi unutmayın!** ⭐
