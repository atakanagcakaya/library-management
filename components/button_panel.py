from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy,
                           QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from textwrap import wrap
from datetime import datetime
from PyQt5.QtGui import QIcon
from src.constants import GENRES, genre_signals

class ButtonPanel(QWidget):
    def __init__(self, data_manager, table_widget, book_section, article_section, magazine_section):
        super().__init__()
        self.data_manager = data_manager
        self.table_widget = table_widget
        self.book_section = book_section
        self.article_section = article_section
        self.magazine_section = magazine_section
        self.setup_ui()
        
        # Connect to genre changes signal
        genre_signals.genre_changed.connect(self.update_genre_list)
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Search bar layout
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("Ara:")
        search_label.setFixedWidth(50)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ara...")
        self.search_input.textChanged.connect(self.search_items)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # Top layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.book_btn = QPushButton("Kitapları Listele")
        self.book_btn.setIcon(QIcon("icons/book.ico"))
        self.article_btn = QPushButton("Makaleleri Listele")
        self.article_btn.setIcon(QIcon("icons/article.ico"))
        self.magazine_btn = QPushButton("Dergileri Listele")
        self.magazine_btn.setIcon(QIcon("icons/magazine.ico"))
        self.excel_btn = QPushButton("Excel")
        self.excel_btn.setIcon(QIcon("icons/excel.ico"))
        self.pdf_btn = QPushButton("PDF")
        self.pdf_btn.setIcon(QIcon("icons/pdf.ico"))
        self.delete_selected_btn = QPushButton("Seçilenleri Sil")
        self.delete_selected_btn.setIcon(QIcon("icons/trash.ico"))
        
        self.book_btn.clicked.connect(self.show_books)
        self.article_btn.clicked.connect(self.show_articles)
        self.magazine_btn.clicked.connect(self.show_magazines)
        self.excel_btn.clicked.connect(self.import_excel)
        self.pdf_btn.clicked.connect(self.export_to_pdf)
        self.delete_selected_btn.clicked.connect(self.table_widget.delete_selected_rows)
        
        button_layout.addWidget(self.book_btn)
        button_layout.addWidget(self.article_btn)
        button_layout.addWidget(self.magazine_btn)
        button_layout.addWidget(self.excel_btn)
        button_layout.addWidget(self.pdf_btn)
        button_layout.addWidget(self.delete_selected_btn)
        button_layout.addStretch()
        
        # Bottom layout for type filter
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        type_label = QLabel("Tür:")
        type_label.setFixedWidth(50)
        
        self.type_combo = QComboBox()
        self.type_combo.setFixedWidth(200)
        
        # Add items to combo box
        self.type_combo.addItem("Hepsi")
        self.type_combo.addItems(sorted(GENRES))
        
        self.type_combo.currentTextChanged.connect(self.filter_by_type)
        
        filter_layout.addWidget(type_label)
        filter_layout.addWidget(self.type_combo)
        filter_layout.addStretch()
        
        # Add layouts to main layout
        main_layout.addLayout(search_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(filter_layout)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 120px;
                icon-size: 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QLabel {
                font-size: 12px;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-height: 25px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-height: 25px;
            }
        """)

    def update_genre_list(self):
        """Update the genre list in combobox when genres change"""
        current_text = self.type_combo.currentText()
        self.type_combo.clear()
        self.type_combo.addItem("Hepsi")
        self.type_combo.addItems(sorted(GENRES))
        
        # Try to restore previous selection
        index = self.type_combo.findText(current_text)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        else:
            self.type_combo.setCurrentIndex(0)

    def get_current_type_turkish(self):
        """Get the Turkish name for the current type."""
        type_map = {
            'book': 'KİTAP',
            'article': 'MAKALE',
            'magazine': 'DERGİ'
        }
        return type_map.get(self.data_manager.current_type, '')

    def get_current_filter_turkish(self):
        """Get the current filter in Turkish."""
        current_filter = self.type_combo.currentText()
        return "HEPSİ" if current_filter == "Hepsi" else current_filter

    def format_current_date(self):
        """Format current date as DD/MM/YYYY."""
        return datetime.now().strftime('%d/%m/%Y')


    # Add this method to your class to get filtered items
    def get_filtered_items(self):
        """Return the currently filtered/displayed items based on selected genre/filter."""
        current_filter = self.type_combo.currentText()
        current_type = self.data_manager.current_type
        
        # Filter items based on genre/type
        filtered_items = []
        for item in self.data_manager.current_items:
            if current_filter == "Hepsi":
                filtered_items.append(item)
            elif item.get("Tür") == current_filter:
                filtered_items.append(item)
                
        return filtered_items

    def filter_by_type(self, selected_type):
        if not self.data_manager.current_items or not self.data_manager.current_type:
            return
            
        if selected_type == "Hepsi":
            filtered_items = self.data_manager.current_items
        else:
            filtered_items = [
                item for item in self.data_manager.current_items 
                if item.get('Tür', '') == selected_type
            ]
            
        self.table_widget.update_table(filtered_items, self.data_manager.current_type)
        
    def show_books(self):
        try:
            if not self.data_manager.books:
                QMessageBox.information(self, "Bilgi", "Henüz kitap kaydı bulunmamaktadır.")
            self.data_manager.current_type = 'book'
            self.data_manager.current_items = self.data_manager.books
            self.filter_by_type(self.type_combo.currentText())
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kitaplar listelenirken hata oluştu: {str(e)}")
            
    def show_articles(self):
        try:
            if not self.data_manager.articles:
                QMessageBox.information(self, "Bilgi", "Henüz makale kaydı bulunmamaktadır.")
            self.data_manager.current_type = 'article'
            self.data_manager.current_items = self.data_manager.articles
            self.filter_by_type(self.type_combo.currentText())
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Makaleler listelenirken hata oluştu: {str(e)}")
            
    def show_magazines(self):
        try:
            if not self.data_manager.magazines:
                QMessageBox.information(self, "Bilgi", "Henüz dergi kaydı bulunmamaktadır.")
            self.data_manager.current_type = 'magazine'
            self.data_manager.current_items = self.data_manager.magazines
            self.filter_by_type(self.type_combo.currentText())
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dergiler listelenirken hata oluştu: {str(e)}")
        
    def import_excel(self):
        try:
            # Create dialog for data type selection
            dialog = QMessageBox()
            dialog.setWindowTitle("Veri Türü Seçin")
            dialog.setText("Excel dosyasındaki veri türünü seçin:")
            dialog.setIcon(QMessageBox.Question)
            
            # Create and configure combo box
            combo = QComboBox()
            combo.addItems(["Kitap", "Makale", "Dergi"])
            combo.setFixedWidth(150)
            dialog.layout().addWidget(combo)
            
            # Add buttons
            dialog.addButton("İptal", QMessageBox.RejectRole)
            ok_button = dialog.addButton("Tamam", QMessageBox.AcceptRole)
            
            # Show dialog
            dialog.exec_()
            
            if dialog.clickedButton() == ok_button:
                data_type = combo.currentText().lower()
                file_path, _ = QFileDialog.getOpenFileName(
                    self, 
                    "Excel Dosyası Seç", 
                    "", 
                    "Excel Files (*.xlsx *.xls)"
                )
                
                if file_path:
                    success, message = self.data_manager.import_excel(file_path, data_type)
                    if success:
                        QMessageBox.information(self, "Başarılı", message)
                        # Update the display based on the imported data type
                        if data_type == 'kitap':
                            self.show_books()
                        elif data_type == 'makale':
                            self.show_articles()
                        else:
                            self.show_magazines()
                    else:
                        QMessageBox.warning(self, "Hata", message)
                        
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel içe aktarma hatası: {str(e)}")

    def search_items(self, text):
        """Filter items based on search text"""
        if not self.data_manager.current_items:
            return
            
        if not text:
            self.filter_by_type(self.type_combo.currentText())
            return
            
        text = text.lower()
        filtered_items = []
        
        for item in self.data_manager.current_items:
            # Search in all text fields
            for value in item.values():
                if isinstance(value, str) and text in value.lower():
                    filtered_items.append(item)
                    break
                    
        self.table_widget.update_table(filtered_items, self.data_manager.current_type)

    def export_to_pdf(self):
        try:
            # Get the currently filtered/displayed items instead of all items
            filtered_items = self.get_filtered_items()  # You'll need to implement this method
            
            if not filtered_items:
                QMessageBox.warning(self, "Uyarı", "Listelenecek veri bulunamadı!")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "PDF Olarak Kaydet", "", "PDF Files (*.pdf)"
            )
            
            if file_path:
                pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
                pdf = canvas.Canvas(file_path, pagesize=A4)
                width, height = A4
                
                # Set margins and spacing - reduce margins to make table wider
                left_margin = 1.5 * cm  # Reduced from 3cm
                right_margin = 1.5 * cm  # Reduced from 3cm
                top_margin = 1.2 * cm
                bottom_margin = 1.2 * cm
                line_height = 15  # Adjusted for better spacing
                
                usable_width = width - left_margin - right_margin
                
                def draw_title(y_pos):
                    pdf.setFont("TimesNewRoman", 16)
                    title = "Kütüphane Yönetim Sistemi"
                    title_width = pdf.stringWidth(title, "TimesNewRoman", 16)
                    # Ensure title is centered properly with more space on sides
                    pdf.drawString((width - title_width) / 2, y_pos, title)
                    
                    # Fixed spacing for subtitle
                    y_pos -= 35
                    
                    # Get the current filter/genre
                    current_type = self.get_current_type_turkish()
                    current_filter = self.get_current_filter_turkish()
                    current_date = self.format_current_date()
                    
                    subtitle = f"{current_type} – {current_filter} – {current_date}"
                    pdf.setFont("TimesNewRoman", 11)
                    subtitle_width = pdf.stringWidth(subtitle, "TimesNewRoman", 11)
                    pdf.drawString((width - subtitle_width) / 2, y_pos, subtitle)
                    
                    # Fixed return value with consistent spacing
                    return y_pos - 35  # Consistent spacing after subtitle

                if self.data_manager.current_type == 'magazine':
                    headers = ["Sıra", "Dergi", "Sayı", "Cilt", "Tarih", "Başlama", "Bitirme"]
                    # Adjusted column proportions for wider table
                    col_props = [0.05, 0.24, 0.09, 0.09, 0.17, 0.17, 0.19]
                else:
                    headers = ["Sıra", "Yazar", 
                            "Kitap" if self.data_manager.current_type == 'book' else "Makale",
                            "Tür", "Başlama", "Bitirme"]
                    col_props = [0.05, 0.22, 0.33, 0.15, 0.125, 0.125]  # Adjusted for wider display

                col_widths = [prop * usable_width for prop in col_props]

                def wrap_text(text, width, font_name, font_size):
                    """Improved text wrapping function to handle long text properly."""
                    pdf.setFont(font_name, font_size)
                    text = str(text)
                    
                    # Handle very long words by breaking them if necessary
                    words = []
                    for word in text.split():
                        if pdf.stringWidth(word, font_name, font_size) > width - 10:
                            # Break long word into chunks
                            current_word = ""
                            for char in word:
                                if pdf.stringWidth(current_word + char, font_name, font_size) > width - 20:
                                    words.append(current_word + "-")
                                    current_word = char
                                else:
                                    current_word += char
                            if current_word:
                                words.append(current_word)
                        else:
                            words.append(word)
                    
                    lines = []
                    current_line = []
                    
                    for word in words:
                        test_line = current_line + [word]
                        line_width = pdf.stringWidth(' '.join(test_line), font_name, font_size)
                        
                        if line_width > width - 10:  # 10 points padding
                            if current_line:  # Only add if we have content
                                lines.append(' '.join(current_line))
                                current_line = [word]
                            else:
                                # Word is too long for a line by itself
                                lines.append(word)
                        else:
                            current_line = test_line
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Ensure we have at least one line
                    if not lines:
                        lines = [""]
                        
                    return lines

                def draw_wrapped_cell(pdf, text, x, y, width, height, font_name, font_size):
                    """Draw cell text with wrapping and vertical centering."""
                    lines = wrap_text(text, width, font_name, font_size)
                    total_lines_height = len(lines) * line_height
                    
                    # Calculate starting position to center text vertically
                    start_y = y - (height - total_lines_height) / 2
                    if start_y > y - line_height:
                        start_y = y - line_height  # Ensure we start with enough space from top
                    
                    # Draw each line of text
                    current_y = start_y
                    for line in lines:
                        text_width = pdf.stringWidth(line, font_name, font_size)
                        x_centered = x + (width - text_width) / 2
                        
                        # Only draw if within cell bounds
                        if current_y > y - height + 2:  # Add a small buffer (2 points)
                            pdf.drawString(x_centered, current_y, line)
                        
                        current_y -= line_height

                def calculate_row_height(row_data, widths, font_name, font_size):
                    """Calculate the maximum height needed for the row."""
                    max_height = line_height
                    for text, width in zip(row_data, widths):
                        lines = wrap_text(text, width, font_name, font_size)
                        height = len(lines) * line_height
                        max_height = max(max_height, height)
                    return max_height + 8  # Added slightly more padding for readability

                def draw_header(y_pos):
                    header_height = 20
                    
                    # Draw header background
                    pdf.setFillColor(colors.Color(0.9, 0.9, 0.9))
                    pdf.rect(left_margin, y_pos - header_height, usable_width, header_height, fill=True, stroke=True)
                    
                    # Draw header text - ensure perfect alignment with columns
                    pdf.setFillColor(colors.black)
                    pdf.setFont("TimesNewRoman", 12)
                    
                    x_position = left_margin
                    for i, (header, width) in enumerate(zip(headers, col_widths)):
                        # Draw cell borders
                        pdf.rect(x_position, y_pos - header_height, width, header_height, stroke=True)
                        
                        # Center text in header cell
                        header_width = pdf.stringWidth(header, "TimesNewRoman", 12)
                        x_centered = x_position + (width - header_width) / 2
                        y_centered = y_pos - (header_height / 2) - 2
                        
                        pdf.drawString(x_centered, y_centered, header)
                        x_position += width
                    
                    # Return a consistent position
                    return y_pos - header_height - 5  # Consistent spacing after header

                # Variable to track if we're on the first page
                is_first_page = True
                
                def new_page():
                    nonlocal is_first_page
                    pdf.showPage()
                    
                    # Start from the same position on each new page
                    y_pos = height - top_margin
                    
                    # Only draw title on the first page
                    if is_first_page:
                        y_pos = draw_title(y_pos)
                        is_first_page = False
                        
                    return draw_header(y_pos)

                y_position = height - top_margin
                # Draw title only on the first page
                y_position = draw_title(y_position)
                # Mark that we've passed the first page for subsequent new pages
                is_first_page = False
                y_position = draw_header(y_position)

                # Use filtered items instead of all items
                for i, item in enumerate(filtered_items, start=1):
                    if self.data_manager.current_type == 'magazine':
                        row_data = [
                            str(i),
                            str(item.get("Dergi", "")),
                            str(item.get("Sayı", "")),
                            str(item.get("Cilt", "")),
                            str(item.get("Tarih", "")),
                            str(item.get("Başlama Tarihi", "")),
                            str(item.get("Bitirme Tarihi", ""))
                        ]
                    else:
                        row_data = [
                            str(i),
                            str(item.get("Yazar", "")),
                            str(item.get("Kitap" if self.data_manager.current_type == 'book' else "Makale", "")),
                            str(item.get("Tür", "")),
                            str(item.get("Başlama Tarihi", "")),
                            str(item.get("Bitirme Tarihi", ""))
                        ]

                    row_height = calculate_row_height(row_data, col_widths, "TimesNewRoman", 10)

                    # Check if we need a new page (with some buffer space to avoid tight fits)
                    if y_position - row_height < bottom_margin + 5:
                        y_position = new_page()

                    # Draw row background for even rows
                    if i % 2 == 0:
                        pdf.setFillColor(colors.Color(0.95, 0.95, 0.95))
                        pdf.rect(left_margin, y_position - row_height, usable_width, row_height, fill=True, stroke=True)

                    # Draw cell contents
                    x_position = left_margin
                    for text, width in zip(row_data, col_widths):
                        # Draw cell border explicitly for each cell
                        pdf.setFillColor(colors.black)
                        pdf.rect(x_position, y_position - row_height, width, row_height, stroke=True)
                        
                        # Draw text with proper vertical alignment
                        draw_wrapped_cell(
                            pdf, text, x_position, y_position, width, row_height,
                            "TimesNewRoman", 10
                        )
                        
                        x_position += width

                    y_position -= row_height

                pdf.save()
                QMessageBox.information(self, "Başarılı", "PDF başarıyla oluşturuldu!")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"PDF oluşturma hatası: {str(e)}")