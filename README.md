# Twitch Video Downloader 🎬

Zaawansowany skrypt Python do pobierania filmów, VOD-ów i klipów z platformy Twitch.tv. Wykorzystuje bibliotekę `yt-dlp` do niezawodnego pobierania treści z różnymi opcjami jakości i metadanych.

## 📋 Spis treści

- [Instalacja](#-instalacja)
- [Szybki start](#-szybki-start)
- [Szczegółowe użycie](#-szczegółowe-użycie)
- [Obsługiwane formaty](#-obsługiwane-formaty)
- [Opcje jakości](#-opcje-jakości)
- [Struktura plików](#-struktura-plików)
- [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
- [API Reference](#-api-reference)
- [Przykłady](#-przykłady)

## 🚀 Instalacja

### Wymagania systemowe

- Python 3.11 lub nowszy
- System operacyjny: Windows, macOS, Linux
- Połączenie internetowe

### Instalacja zależności

```bash
pip install yt-dlp
```

### Pobieranie skryptu

1. Skopiuj kod skryptu do pliku `twitch_downloader.py`
2. Nadaj uprawnienia wykonywania (Linux/macOS):
   ```bash
   chmod +x twitch_downloader.py
   ```

## ⚡ Szybki start

### Tryb interaktywny
```bash
python twitch_downloader.py
```

### Użycie z argumentami
```bash
# Podstawowe użycie
python twitch_downloader.py "https://www.twitch.tv/videos/2465592622"

# Z określoną jakością
python twitch_downloader.py "https://www.twitch.tv/videos/2465592622" "720p"
```

## 📖 Szczegółowe użycie

### Tryb interaktywny

Po uruchomieniu skryptu bez argumentów, zostaniesz poproszony o:

1. **URL filmu** - Wklej link do filmu z Twitcha
2. **Jakość pobierania** - Wybierz jedną z dostępnych opcji

#### Przykład sesji interaktywnej:
```
🎬 Twitch Video Downloader
==============================
Wprowadź URL filmu z Twitcha:
URL: https://www.twitch.tv/videos/2465592622

Dostępne jakości:
1. best (najlepsza dostępna, max 1080p)
2. 1080p
3. 720p
4. 480p
5. 360p
6. audio (tylko dźwięk)
7. best + napisy (może powodować błędy)

Wybierz jakość (1-7) lub wciśnij Enter dla domyślnej: 2
```

### Tryb z argumentami

```bash
python twitch_downloader.py [URL] [JAKOŚĆ]
```

**Parametry:**
- `URL` - Link do filmu na Twitchu (wymagany)
- `JAKOŚĆ` - Opcjonalna jakość filmu (domyślnie: `best`)

## 🎯 Obsługiwane formaty

Skrypt obsługuje następujące typy linków z Twitcha:

### VOD (Video on Demand)
```
https://www.twitch.tv/videos/123456789
https://www.twitch.tv/username/video/123456789
```

### Klipy
```
https://clips.twitch.tv/ClipName
https://www.twitch.tv/username/clip/ClipName
```

### Przykłady prawidłowych URL:
- `https://www.twitch.tv/videos/2465592622`
- `https://clips.twitch.tv/FamousCleverSalamanderNotATK`
- `https://www.twitch.tv/sodapoppin/clip/PowerfulHelplessCodSSSsss`

## 🎥 Opcje jakości

| Opcja | Opis | Format |
|-------|------|--------|
| `best` | Najlepsza dostępna (max 1080p) | Video + Audio |
| `1080p` | Full HD (jeśli dostępne) | Video + Audio |
| `720p` | HD | Video + Audio |
| `480p` | SD | Video + Audio |
| `360p` | Niska jakość | Video + Audio |
| `audio` | Tylko dźwięk | Audio only |
| `worst` | Najniższa jakość | Video + Audio |

### Automatyczny wybór jakości

Skrypt automatycznie wybiera najlepszą dostępną jakość w ramach określonego limitu. Jeśli wybierzesz `1080p`, a film dostępny jest tylko w `720p`, zostanie pobrana jakość `720p`.

## 📁 Struktura plików

### Katalog docelowy
Domyślnie pliki są zapisywane w katalogu `downloads/` w lokalizacji skryptu.

### Nazewnictwo plików
```
[Nazwa_kanału]_[Tytuł_filmu]_[ID_filmu].[rozszerzenie]
```

#### Przykład:
```
vigoletto_⭐Dołączcie do czatu! Kultowy czwartek !ETS2 !Driving !Simulator !chat !tiktok_v2465592622.mp4
```

### Dodatkowe pliki

Skrypt może tworzyć następujące dodatkowe pliki:

- **`.info.json`** - Metadane filmu (tytuł, opis, statystyki)
- **`.rechat.json`** - Napisy/czat (jeśli dostępne i włączone)

## 🔧 Rozwiązywanie problemów

### Częste błędy i rozwiązania

#### 1. Błąd 404 - Film nie znaleziony
```
❌ Film nie został znaleziony (404). Sprawdź czy URL jest prawidłowy i film nadal istnieje.
```

**Rozwiązanie:**
- Sprawdź poprawność URL
- Zweryfikuj czy film nadal istnieje na Twitchu
- Niektóre stare filmy mogą być niedostępne

#### 2. Błąd 403 - Brak dostępu
```
❌ Brak dostępu do filmu (403). Film może być prywatny lub zablokowany.
```

**Rozwiązanie:**
- Film może być prywatny
- Streamer mógł ograniczyć dostęp
- Spróbuj z innym filmem

#### 3. Błędy z napisami
```
❌ Błąd związany z napisami. Film może nie mieć dostępnych napisów.
```

**Rozwiązanie:**
- Skrypt automatycznie spróbuje ponownie bez napisów
- Użyj opcji 1-6 zamiast opcji 7

#### 4. Brak modułu yt-dlp
```
ModuleNotFoundError: No module named 'yt_dlp'
```

**Rozwiązanie:**
```bash
pip install yt-dlp
```

### Debugging

Aby uzyskać więcej informacji o błędach, możesz uruchomić skrypt z dodatkowym logowaniem:

```python
# Dodaj na początku main()
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 API Reference

### Klasa TwitchDownloader

#### `__init__(download_dir="downloads")`

Inicjalizuje downloader z określonym katalogiem docelowym.

**Parametry:**
- `download_dir` (str): Katalog docelowy dla pobranych plików

#### `is_valid_twitch_url(url)`

Sprawdza czy podany URL jest prawidłowym linkiem Twitcha.

**Parametry:**
- `url` (str): URL do sprawdzenia

**Zwraca:**
- `bool`: True jeśli URL jest prawidłowy

#### `get_video_info(url)`

Pobiera informacje o filmie bez pobierania.

**Parametry:**
- `url` (str): URL filmu

**Zwraca:**
- `dict`: Słownik z informacjami o filmie lub None w przypadku błędu

#### `download_video(url, quality='best', download_subtitles=False)`

Główna metoda pobierająca film.

**Parametry:**
- `url` (str): URL filmu
- `quality` (str): Jakość filmu
- `download_subtitles` (bool): Czy pobierać napisy

**Zwraca:**
- `bool`: True jeśli pobieranie zakończone sukcesem

## 💡 Przykłady

### Przykład 1: Podstawowe pobieranie
```python
from twitch_downloader import TwitchDownloader

downloader = TwitchDownloader()
url = "https://www.twitch.tv/videos/2465592622"
success = downloader.download_video(url)

if success:
    print("Film został pobrany!")
```

### Przykład 2: Pobieranie z określoną jakością
```python
downloader = TwitchDownloader("./moje_filmy")
url = "https://www.twitch.tv/videos/2465592622"
success = downloader.download_video(url, quality="720p")
```

### Przykład 3: Sprawdzanie informacji przed pobraniem
```python
downloader = TwitchDownloader()
url = "https://www.twitch.tv/videos/2465592622"

# Sprawdź informacje
info = downloader.get_video_info(url)
if info:
    print(f"Tytuł: {info['title']}")
    print(f"Czas trwania: {info['duration']} sekund")
    
    # Pobierz jeśli film jest krótszy niż 2 godziny
    if info['duration'] < 7200:
        downloader.download_video(url)
```

### Przykład 4: Masowe pobieranie
```python
urls = [
    "https://www.twitch.tv/videos/2465592622",
    "https://clips.twitch.tv/ExampleClip",
    "https://www.twitch.tv/videos/1234567890"
]

downloader = TwitchDownloader()

for url in urls:
    if downloader.is_valid_twitch_url(url):
        print(f"Pobieranie: {url}")
        downloader.download_video(url, quality="720p")
    else:
        print(f"Nieprawidłowy URL: {url}")
```

## 🤝 Wsparcie

### Zgłaszanie błędów

Jeśli napotkasz problem:

1. Sprawdź sekcję [Rozwiązywanie problemów](#-rozwiązywanie-problemów)
2. Upewnij się, że masz najnowszą wersję `yt-dlp`
3. Sprawdź czy URL jest prawidłowy i film istnieje

### Aktualizacje

Aby zaktualizować `yt-dlp` do najnowszej wersji:

```bash
pip install --upgrade yt-dlp
```

## ⚖️ Informacje prawne

- Szanuj prawa autorskie i regulamin Twitcha
- Pobieraj tylko treści, do których masz prawo
- Nie rozpowszechniaj pobranych treści bez zgody autorów
- Skrypt jest przeznaczony do użytku osobistego

## 📄 Licencja

Ten skrypt jest udostępniony w celach edukacyjnych i osobistych. Użytkownicy są odpowiedzialni za przestrzeganie wszystkich obowiązujących przepisów prawa i regulaminów platform.

---

**Wersja dokumentacji:** 1.0  
**Data ostatniej aktualizacji:** Maj 2025  
**Kompatybilność:** Python 3.11+, yt-dlp 2024.x+
