from typing import List
import json
import os
from PyQt5.QtCore import pyqtSignal, QObject

# Create a signal emitter class for genre changes
class GenreSignals(QObject):
    genre_changed = pyqtSignal()

genre_signals = GenreSignals()

TURKISH_MONTHS = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}

def load_genres() -> List[str]:
    """Load genres from file or return default list"""
    file_path = "genres.json"
    default_genres = [
        "Anı", "Askeri", "Bilim", "Dil", "Din",
        "Ekonomi", "Eleştiri", "Felsefe", "Günce Yazılar",
        "Hikaye/Öykü", "Roman", "Sanat", "Senaryo",
        "Siyaset", "Şiir", "Tarih", "Tiyatro", "Edebiyat"
    ]
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sorted(json.load(f))
        except:
            return default_genres
    else:
        save_genres(default_genres)
        return default_genres

def save_genres(genres: List[str]):
    """Save genres to file"""
    with open("genres.json", 'w', encoding='utf-8') as f:
        json.dump(sorted(list(set(genres))), f, ensure_ascii=False, indent=2)

def add_genre(genre: str) -> bool:
    """Add a new genre to the list"""
    genres = load_genres()
    if genre not in genres:
        genres.append(genre)
        save_genres(genres)
        # Emit signal that genres have changed
        genre_signals.genre_changed.emit()
        return True
    return False

def delete_genre(genre: str) -> bool:
    """Delete a genre from the list"""
    genres = load_genres()
    if genre in genres:
        genres.remove(genre)
        save_genres(genres)
        # Emit signal that genres have changed
        genre_signals.genre_changed.emit()
        return True
    return False

# Initialize the GENRES list
GENRES: List[str] = load_genres()