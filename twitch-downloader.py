import os
import sys
import re
from pathlib import Path
import yt_dlp
from urllib.parse import urlparse

class TwitchDownloader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        self.ydl_opts = {
            'outtmpl': str(self.download_dir / '%(uploader)s_%(title)s_%(id)s.%(ext)s'),
            'format': 'best[height<=1080]',
            'writeinfojson': True,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': True,
            'no_warnings': False,
        }
    
    def is_valid_twitch_url(self, url):
        twitch_patterns = [
            r'https?://(?:www\.)?twitch\.tv/videos/\d+',
            r'https?://(?:www\.)?twitch\.tv/\w+/video/\d+',
            r'https?://clips\.twitch\.tv/\w+',
            r'https?://(?:www\.)?twitch\.tv/\w+/clip/\w+',
        ]
        
        return any(re.match(pattern, url) for pattern in twitch_patterns)
    
    def get_video_info(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Nieznany tytuł'),
                    'uploader': info.get('uploader', 'Nieznany kanał'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Nieznana data'),
                    'description': info.get('description', ''),
                    'formats': len(info.get('formats', [])),
                }
        except Exception as e:
            print(f"Błąd podczas pobierania informacji: {e}")
            return None
    
    def download_video(self, url, quality='best', download_subtitles=False):
        if not self.is_valid_twitch_url(url):
            print("❌ Nieprawidłowy URL Twitcha!")
            return False
        
        format_selector = self._get_format_selector(quality)
        current_opts = self.ydl_opts.copy()
        current_opts['format'] = format_selector
        
        if download_subtitles:
            current_opts['writesubtitles'] = True
            current_opts['writeautomaticsub'] = True
            print("⚠️  Uwaga: Pobieranie napisów może powodować błędy na niektórych filmach Twitcha")
        
        try:
            print(f"🔍 Analizuję film...")
            info = self.get_video_info(url)
            
            if info:
                print(f"📹 Tytuł: {info['title']}")
                print(f"👤 Kanał: {info['uploader']}")
                print(f"⏱️  Czas trwania: {self._format_duration(info['duration'])}")
                print(f"👁️  Wyświetlenia: {info['view_count']:,}")
                print(f"📅 Data: {info['upload_date']}")
                print(f"🎥 Dostępne formaty: {info['formats']}")
                print()
            
            print(f"⬇️  Rozpoczynam pobieranie z jakością: {quality}")
            
            current_opts.update({
                'extract_flat': False,
                'writeinfojson': True,
                'writethumbnail': False,
                'embed_subs': False,
            })
            
            with yt_dlp.YoutubeDL(current_opts) as ydl:
                try:
                    ydl.download([url])
                except yt_dlp.DownloadError as download_error:
                    if "subtitles" in str(download_error).lower() or "rechat" in str(download_error).lower():
                        print("⚠️  Błąd z napisami, próbuję ponownie bez napisów...")
                        current_opts['writesubtitles'] = False
                        current_opts['writeautomaticsub'] = False
                        with yt_dlp.YoutubeDL(current_opts) as ydl_retry:
                            ydl_retry.download([url])
                    else:
                        raise download_error
            
            print("✅ Pobieranie zakończone pomyślnie!")
            return True
            
        except yt_dlp.DownloadError as e:
            error_msg = str(e)
            if "HTTP Error 404" in error_msg:
                print("❌ Film nie został znaleziony (404). Sprawdź czy URL jest prawidłowy i film nadal istnieje.")
            elif "HTTP Error 403" in error_msg:
                print("❌ Brak dostępu do filmu (403). Film może być prywatny lub zablokowany.")
            elif "subtitles" in error_msg.lower():
                print("❌ Błąd związany z napisami. Film może nie mieć dostępnych napisów.")
            else:
                print(f"❌ Błąd pobierania: {e}")
            return False
        except Exception as e:
            print(f"❌ Nieoczekiwany błąd: {e}")
            return False
    
    def _get_format_selector(self, quality):
        """
        Zwraca selektor formatu na podstawie żądanej jakości
        """
        quality_map = {
            'best': 'best[height<=1080]',
            'worst': 'worst',
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            '360p': 'best[height<=360]',
            'audio': 'bestaudio',
        }
        
        return quality_map.get(quality.lower(), 'best[height<=1080]')
    
    def _format_duration(self, seconds):
        """
        Formatuje czas trwania w sekundach na czytelny format
        """
        if not seconds:
            return "Nieznany"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

def main():
    print("🎬 Twitch Video Downloader")
    print("=" * 30)
    
    downloader = TwitchDownloader()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        quality = sys.argv[2] if len(sys.argv) > 2 else 'best'
    else:
        print("Wprowadź URL filmu z Twitcha:")
        url = input("URL: ").strip()
        
        print("\nDostępne jakości:")
        print("1. best (najlepsza dostępna, max 1080p)")
        print("2. 1080p")
        print("3. 720p")
        print("4. 480p")
        print("5. 360p")
        print("6. audio (tylko dźwięk)")
        print("7. best + napisy (może powodować błędy)")
        
        choice = input("\nWybierz jakość (1-7) lub wciśnij Enter dla domyślnej: ").strip()
        
        quality_map = {
            '1': 'best',
            '2': '1080p',
            '3': '720p',
            '4': '480p',
            '5': '360p',
            '6': 'audio',
            '7': 'best',
        }
        
        quality = quality_map.get(choice, 'best')
        download_subtitles = choice == '7'
    
    if not url:
        print("❌ Nie podano URL!")
        return
    
    print(f"\n🎯 URL: {url}")
    print(f"🎥 Jakość: {quality}")
    print(f"📁 Katalog docelowy: {downloader.download_dir.absolute()}")
    print()
    
    if 'download_subtitles' in locals():
        success = downloader.download_video(url, quality, download_subtitles)
    else:
        success = downloader.download_video(url, quality)
    
    if success:
        print(f"\n📁 Pliki zostały zapisane w: {downloader.download_dir.absolute()}")
    else:
        print("\n❌ Pobieranie nie powiodło się!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Przerwano przez użytkownika")
    except Exception as e:
        print(f"\n❌ Krytyczny błąd: {e}")