from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox, QComboBox,
                           QInputDialog, QSizePolicy, QMenu)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from datetime import datetime
from src.constants import GENRES, add_genre, delete_genre, genre_signals

class BaseSection(QWidget):
    def __init__(self, title, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setup_ui(title)
        
        # Connect to genre changes signal
        genre_signals.genre_changed.connect(self.update_genre_list)
        
    def setup_ui(self, title):
        # Set fixed size for the entire section
        self.setFixedSize(430, 350)  # Adjust these values based on your needs
        
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 10px;
            }
            QLabel {
                background: transparent;
                color: #333;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 5px 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
                min-height: 20px;
                max-height: 25px;
            }
            QComboBox {
                padding: 5px 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
                min-height: 20px;
                max-height: 25px;
                min-width: 200px;
                max-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: url(icons/chevron-down.ico);
                width: 12px;
                height: 12px;
            }
            QPushButton {
                border-radius: 12px;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton#addBtn {
                background-color: transparent;
                border: none;
            }
            QPushButton#clearBtn {
                background-color: transparent;
                border: none;
            }
            QPushButton#genreBtn {
                background-color: transparent;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QPushButton#genreBtn:hover {
                background-color: #f0f0f0;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setAlignment(Qt.AlignTop)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            background: #e0e0e0;
            font-weight: bold;
            font-size: 14px;
            color: #2c3e50;
            padding: 8px;
            border-radius: 10px;
            text-align: center;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFixedHeight(35)
        main_layout.addWidget(title_label)

        # Content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setAlignment(Qt.AlignTop)

        self.inputs = {}
        self.setup_inputs(content_layout)
        
        main_layout.addWidget(content_widget)
        
        # Buttons layout at the bottom
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        self.add_btn = QPushButton()
        self.add_btn.setIcon(QIcon("icons/check.ico"))
        self.add_btn.setObjectName("addBtn")
        self.add_btn.setToolTip("Ekle")
        
        self.clear_btn = QPushButton()
        self.clear_btn.setIcon(QIcon("icons/clear.ico"))
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setToolTip("Temizle")
        self.clear_btn.clicked.connect(self.clear_inputs)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
    def create_input_row(self, label, input_field):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        row_layout.setContentsMargins(0, 0, 0, 0)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setFixedWidth(120)
        label_widget.setFixedHeight(42)
        
        # Input field setup
        if isinstance(input_field, QComboBox):
            input_container = QWidget()
            container_layout = QHBoxLayout(input_container)
            container_layout.setSpacing(5)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            input_field.setFixedSize(150, 25)
            container_layout.addWidget(input_field)
            
            if label == 'Tür':
                # Create a button with a menu for genre operations
                genre_btn = QPushButton()
                genre_btn.setIcon(QIcon("icons/menu.ico"))
                genre_btn.setObjectName("genreBtn")
                genre_btn.setToolTip("Tür İşlemleri")
                genre_btn.setFixedSize(25, 25)
                
                # Create context menu for the button
                genre_menu = QMenu(self)
                add_action = genre_menu.addAction(QIcon("icons/plus.ico"), "Yeni Tür Ekle")
                delete_action = genre_menu.addAction(QIcon("icons/trash.ico"), "Tür Sil")
                
                # Connect actions
                add_action.triggered.connect(self.add_new_genre)
                delete_action.triggered.connect(self.delete_genre)
                
                # Show menu when button is clicked
                genre_btn.clicked.connect(lambda: genre_menu.exec_(genre_btn.mapToGlobal(genre_btn.rect().bottomLeft())))
                
                container_layout.addWidget(genre_btn)
            
            container_layout.addStretch()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_container)
        else:
            input_field.setFixedHeight(25)
            input_field.setFixedWidth(200)
            
            if "Tarih" in label:
                input_field.setPlaceholderText("GG/AA/YYYY")
                input_field.setAlignment(Qt.AlignCenter)
            elif label in ["Sayı", "Cilt"]:
                label_widget.setFixedWidth(50)
                input_field.setFixedWidth(100)
            
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_field)
            row_layout.addStretch()
        
        return row_layout  # Return the layout instead of a widget
    
    def update_genre_list(self):
        """Update the genre list in combobox when genres change"""
        if 'Tür' in self.inputs and isinstance(self.inputs['Tür'], QComboBox):
            current_text = self.inputs['Tür'].currentText()
            self.inputs['Tür'].clear()
            self.inputs['Tür'].addItems(sorted(GENRES))
            
            # Try to restore previous selection
            index = self.inputs['Tür'].findText(current_text)
            if index >= 0:
                self.inputs['Tür'].setCurrentIndex(index)
        
    def add_new_genre(self):
        genre, ok = QInputDialog.getText(
            self, 
            "Yeni Tür Ekle",
            "Tür adını girin:",
            QLineEdit.Normal
        )
        
        if ok and genre:
            genre = genre.strip()
            if add_genre(genre):
                QMessageBox.information(self, "Başarılı", f"'{genre}' türü eklendi.")
            else:
                QMessageBox.warning(self, "Uyarı", f"'{genre}' türü zaten mevcut.")
    
    def delete_genre(self):
        """Delete a genre from the list"""
        if not GENRES:
            QMessageBox.warning(self, "Uyarı", "Silinecek tür bulunamadı!")
            return
            
        genre, ok = QInputDialog.getItem(
            self,
            "Tür Sil",
            "Silinecek türü seçin:",
            sorted(GENRES),
            0,
            False
        )
        
        if ok and genre:
            confirm = QMessageBox.question(
                self,
                "Onay",
                f"'{genre}' türünü silmek istediğinizden emin misiniz?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirm == QMessageBox.Yes:
                if delete_genre(genre):
                    QMessageBox.information(self, "Başarılı", f"'{genre}' türü silindi.")
                else:
                    QMessageBox.warning(self, "Hata", f"'{genre}' türü silinemedi.")
        
    def setup_inputs(self, layout):
        raise NotImplementedError("Subclasses must implement setup_inputs")
        
    def clear_inputs(self):
        for input_field in self.inputs.values():
            if isinstance(input_field, QLineEdit):
                input_field.clear()
            elif isinstance(input_field, QComboBox):
                input_field.setCurrentIndex(0)
            
    def validate_date(self, date_str, is_month_year=False):
        if not date_str:
            return True
            
        try:
            if is_month_year:
                # Try parsing as month/year format
                datetime.strptime(date_str, '%m/%Y')
            else:
                # Try parsing as full date format
                datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False
            
    def validate_inputs(self):
        empty_fields = []
        invalid_dates = []
        
        for label, input_field in self.inputs.items():
            value = input_field.text().strip() if isinstance(input_field, QLineEdit) else input_field.currentText()
            
            if not value:
                empty_fields.append(label)
            elif label == 'Tarih':
                # Validate month/year format for magazine date
                if not self.validate_date(value, is_month_year=True):
                    invalid_dates.append(f"{label} (AA/YYYY formatında)")
            elif 'Tarihi' in label:
                # Validate full date format for start/end dates
                if not self.validate_date(value):
                    invalid_dates.append(f"{label} (GG/AA/YYYY formatında)")
                
        if empty_fields:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                f"Lütfen aşağıdaki alanları doldurun:\n- {'\n- '.join(empty_fields)}"
            )
            return False
            
        if invalid_dates:
            QMessageBox.warning(
                self,
                "Geçersiz Tarih",
                f"Lütfen aşağıdaki tarihleri doğru formatta girin:\n- {'\n- '.join(invalid_dates)}"
            )
            return False
            
        return True