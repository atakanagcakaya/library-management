import os
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import uuid

class DataManager(QObject):
    genre_added = pyqtSignal()  # Signal for when a new genre is added
    
    def __init__(self):
        super(DataManager, self).__init__()  # Properly initialize QObject
        self.books = []
        self.articles = []
        self.magazines = []
        self.current_type = None
        self.current_items = []

    def save_data(self):
        data = {
            'books': self.books,
            'articles': self.articles,
            'magazines': self.magazines
        }
        pd.to_pickle(data, "library_data.pkl")

    def load_data(self):
        if os.path.exists("library_data.pkl"):
            data = pd.read_pickle("library_data.pkl")
            self.books = data.get('books', [])
            self.articles = data.get('articles', [])
            self.magazines = data.get('magazines', [])
            
            # Ensure all items have IDs
            for item_list in [self.books, self.articles, self.magazines]:
                for item in item_list:
                    if 'id' not in item:
                        item['id'] = str(uuid.uuid4())

    def add_book(self, book_data):
        # Ensure book has an ID
        if 'id' not in book_data:
            book_data['id'] = str(uuid.uuid4())
            
        self.books.append(book_data)
        self.save_data()

    def add_article(self, article_data):
        # Ensure article has an ID
        if 'id' not in article_data:
            article_data['id'] = str(uuid.uuid4())
            
        self.articles.append(article_data)
        self.save_data()

    def add_magazine(self, magazine_data):
        # Ensure magazine has an ID
        if 'id' not in magazine_data:
            magazine_data['id'] = str(uuid.uuid4())
            
        self.magazines.append(magazine_data)
        self.save_data()

    def delete_item(self, row):
        if self.current_type == 'book':
            del self.books[row]
        elif self.current_type == 'article':
            del self.articles[row]
        elif self.current_type == 'magazine':
            del self.magazines[row]
        else:
            return
            
        self.save_data()

    def format_date(self, date_value):
        if pd.isna(date_value):
            return ""
        
        try:
            # Try parsing as datetime first
            if isinstance(date_value, pd.Timestamp):
                return date_value.strftime('%d/%m/%Y')
                
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',      # 2023-12-31
                '%d.%m.%Y',      # 31.12.2023
                '%d/%m/%Y',      # 31/12/2023
                '%Y/%m/%d',      # 2023/12/31
                '%d-%m-%Y',      # 31-12-2023
                '%Y.%m.%d'       # 2023.12.31
            ]
            
            for date_format in date_formats:
                try:
                    parsed_date = datetime.strptime(str(date_value).strip(), date_format)
                    return parsed_date.strftime('%d/%m/%Y')
                except ValueError:
                    continue
                    
            # If all parsing fails, return the original value as string
            return str(date_value)
        except Exception:
            return str(date_value)

    def import_excel(self, file_path, data_type):
        try:
            df = pd.read_excel(file_path)
            
            # Convert column names to lowercase and strip whitespace
            df.columns = df.columns.str.strip().str.lower()
            
            if data_type == "kitap":
                for _, row in df.iterrows():
                    self.add_book({
                        "Yazar": str(row.get("yazar", "")),
                        "Kitap": str(row.get("kitap", "")),
                        "Tür": str(row.get("tür", "")),
                        "Başlama Tarihi": self.format_date(row.get("başlama tarihi", "")),
                        "Bitirme Tarihi": self.format_date(row.get("bitirme tarihi", "")),
                        "type": "book",
                        "id": str(uuid.uuid4())
                    })
            elif data_type == "makale":
                for _, row in df.iterrows():
                    self.add_article({
                        "Yazar": str(row.get("yazar", "")),
                        "Makale": str(row.get("makale", "")),
                        "Tür": str(row.get("tür", "")),
                        "Başlama Tarihi": self.format_date(row.get("başlama tarihi", "")),
                        "Bitirme Tarihi": self.format_date(row.get("bitirme tarihi", "")),
                        "type": "article",
                        "id": str(uuid.uuid4())
                    })
            elif data_type == "dergi":
                for _, row in df.iterrows():
                    self.add_magazine({
                        "Dergi": str(row.get("dergi", "")),
                        "Sayı": str(row.get("sayı", "")),
                        "Cilt": str(row.get("cilt", "")),
                        "Tarih": self.format_date(row.get("tarih", "")),
                        "Başlama Tarihi": self.format_date(row.get("başlama tarihi", "")),
                        "Bitirme Tarihi": self.format_date(row.get("bitirme tarihi", "")),
                        "type": "magazine",
                        "id": str(uuid.uuid4())
                    })
            
            return True, "Excel verisi başarıyla yüklendi!"
        except Exception as e:
            return False, f"Veri yükleme hatası: {str(e)}"