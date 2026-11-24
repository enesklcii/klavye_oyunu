# Ekran Ayarları
WIDTH = 850
HEIGHT = 720
FPS = 60

# Renkler (RGB - Neon Uzay Teması)
BG_COLOR = (10, 12, 24)
GRID_COLOR = (20, 26, 46)
WHITE = (240, 244, 255)
NEON_GREEN = (57, 255, 20)
NEON_CYAN = (0, 229, 255)
NEON_RED = (255, 49, 88)
NEON_PURPLE = (185, 80, 255)
GOLD = (255, 215, 0)

# Oyun Mekaniği
INITIAL_LIVES = 5
INITIAL_SPAWN_DELAY = 1900
BASE_FALL_SPEED = 1.0
HIGHSCORE_FILE = "highscore.json"

# Özel Güçlendirme Kelimeleri
POWERUP_WORDS = {
    "bomba": "BOMB",       # Ekrandaki tüm kelimeleri temizler
    "yavaslat": "SLOW",    # 5 saniye boyunca kelimeleri yavaşlatır
    "kalkan": "HEAL"       # +1 Can verir
}

# Normal Kelime Havuzu
WORD_LIST = [
    "python", "algoritma", "fonksiyon", "degisken", "klavye", "yazilim",
    "veritabani", "sunucu", "bulut", "yapayzeka", "sistem", "kodlama",
    "terminal", "paket", "modul", "liste", "sozluk", "dongu", "kosul",
    "sinif", "nesne", "miras", "hata", "cozum", "hizli", "parmak",
    "odak", "basari", "proje", "github", "commit", "branch", "deploy",
    "docker", "linux", "network", "guvenlik", "sifre", "anahtar", "vektor",
    "uzay", "lazer", "roket", "yildiz", "galaksi", "evren", "frekans",
    "islemci", "bellek", "arayuz", "sunum", "mimari", "performans"
]
