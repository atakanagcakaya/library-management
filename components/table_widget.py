from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, QPushButton, 
                           QHeaderView, QWidget, QHBoxLayout, QMessageBox,
                           QAbstractItemView, QSizePolicy)
from PyQt5.QtCore import Qt
from datetime import datetime
from src.constants import TURKISH_MONTHS
from PyQt5.QtGui import QIcon

class TableWidget(QTableWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QPushButton {
                background-color: transparent;
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
                min-width: 30px;
                max-width: 30px;
                min-height: 25px;
                max-height: 25px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        # Enable multiple selection
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # Initialize with default columns
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "Sıra No", "Yazar", "Kitap/Makale/Dergi", "Tür", 
            "Başlama Tarihi", "Bitirme Tarihi"
        ])
        
        # Set header properties
        header = self.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        
        # Allow user to resize columns
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        # Set specific column widths
        self.setColumnWidth(0, 70)  # Sıra No
        self.setColumnWidth(1, 200)  # Yazar
        self.setColumnWidth(2, 250)  # Kitap/Makale/Dergi
        self.setColumnWidth(3, 150)  # Tür
        self.setColumnWidth(4, 120)  # Başlama Tarihi
        self.setColumnWidth(5, 120)  # Bitirme Tarihi
        
        # Make other columns stretch to fill space
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        # Hide vertical header (row numbers)
        self.verticalHeader().setVisible(False)
        
        # Enable alternating row colors
        self.setAlternatingRowColors(True)
        self.setShowGrid(True)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_table(self, items, current_type):
        """Update the table with the given items."""
        try:
            self.setRowCount(0)  # Clear existing rows
            if not items:
                return
                
            self.setRowCount(len(items))
            
            if current_type == 'magazine':
                self.setup_magazine_table(items)
            else:
                self.setup_book_article_table(items, current_type)
                
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Tablo güncellenirken hata oluştu: {str(e)}")

    def format_date(self, date_str, is_month_year=False):
        if not date_str:
            return ""
            
        try:
            if is_month_year:
                # Convert MM/YYYY to Turkish Month YYYY format
                try:
                    # First try with MM/YYYY format
                    date = datetime.strptime(date_str, '%m/%Y')
                    month_num = date.month
                    turkish_month = TURKISH_MONTHS.get(month_num, '')
                    return f"{turkish_month} {date.year}"
                except ValueError:
                    # If that fails, try with YYYY-MM-DD format and extract month/year
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        month_num = date.month
                        turkish_month = TURKISH_MONTHS.get(month_num, '')
                        return f"{turkish_month} {date.year}"
                    except ValueError:
                        # If all parsing fails, return original
                        return date_str
            else:
                # Try different date formats for full dates
                try:
                    # First try with DD/MM/YYYY format
                    date = datetime.strptime(date_str, '%d/%m/%Y')
                    return date.strftime('%d/%m/%Y')
                except ValueError:
                    # Then try with YYYY-MM-DD format
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        return date.strftime('%d/%m/%Y')
                    except ValueError:
                        # If all parsing fails, return original
                        return date_str
        except Exception:
            return date_str

    def create_centered_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def setup_magazine_table(self, items):
        headers = ["Sıra No", "Dergi", "Sayı", "Cilt", "Tarih", "Başlama Tarihi", "Bitirme Tarihi"]
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths for magazine table
        self.setColumnWidth(0, 70)  # Sıra No
        self.setColumnWidth(1, 200)  # Dergi
        self.setColumnWidth(2, 80)  # Sayı
        self.setColumnWidth(3, 80)  # Cilt
        self.setColumnWidth(4, 120)  # Tarih
        self.setColumnWidth(5, 120)  # Başlama Tarihi
        self.setColumnWidth(6, 120)  # Bitirme Tarihi
        
        # Set stretch for content column
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Make Dergi column stretch

        for row, item in enumerate(items):
            self.setItem(row, 0, self.create_centered_item(str(row + 1)))
            self.setItem(row, 1, QTableWidgetItem(str(item.get('Dergi', ''))))
            self.setItem(row, 2, self.create_centered_item(str(item.get('Sayı', ''))))
            self.setItem(row, 3, self.create_centered_item(str(item.get('Cilt', ''))))
            self.setItem(row, 4, self.create_centered_item(
                self.format_date(str(item.get('Tarih', '')), is_month_year=True)
            ))
            self.setItem(row, 5, self.create_centered_item(
                self.format_date(str(item.get('Başlama Tarihi', '')))
            ))
            self.setItem(row, 6, self.create_centered_item(
                self.format_date(str(item.get('Bitirme Tarihi', '')))
            ))
            
    def setup_book_article_table(self, items, current_type):
        headers = ["Sıra No", "Yazar", "Kitap" if current_type == 'book' else "Makale", 
                  "Tür", "Başlama Tarihi", "Bitirme Tarihi"]
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(headers)
        
        # Set column widths for book/article table
        self.setColumnWidth(0, 70)  # Sıra No
        self.setColumnWidth(1, 200)  # Yazar
        self.setColumnWidth(2, 250)  # Kitap/Makale
        self.setColumnWidth(3, 150)  # Tür
        self.setColumnWidth(4, 120)  # Başlama Tarihi
        self.setColumnWidth(5, 120)  # Bitirme Tarihi
        
        # Set stretch for content column
        header = self.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Make content column stretch

        for row, item in enumerate(items):
            self.setItem(row, 0, self.create_centered_item(str(row + 1)))
            self.setItem(row, 1, QTableWidgetItem(str(item.get('Yazar', ''))))
            self.setItem(row, 2, QTableWidgetItem(str(item.get('Kitap' if current_type == 'book' else 'Makale', ''))))
            self.setItem(row, 3, QTableWidgetItem(str(item.get('Tür', ''))))
            self.setItem(row, 4, self.create_centered_item(
                self.format_date(str(item.get('Başlama Tarihi', '')))
            ))
            self.setItem(row, 5, self.create_centered_item(
                self.format_date(str(item.get('Bitirme Tarihi', '')))
            ))
            
    def delete_selected_rows(self):
        selected_rows = sorted(set(item.row() for item in self.selectedItems()), reverse=True)
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek satırları seçin!")
            return
            
        confirm = QMessageBox.question(
            self,
            "Onay",
            f"Seçili {len(selected_rows)} satırı silmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                for row in selected_rows:
                    self.data_manager.delete_item(row)
                self.update_table(self.data_manager.current_items, self.data_manager.current_type)
                QMessageBox.information(self, "Başarılı", "Seçili satırlar başarıyla silindi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Satırlar silinirken hata oluştu: {str(e)}")