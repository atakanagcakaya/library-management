from PyQt5.QtWidgets import QLineEdit, QComboBox
from .base_section import BaseSection
from src.constants import GENRES, add_genre

class BookSection(BaseSection):
    def __init__(self, data_manager):
        super().__init__("Kitap", data_manager)
        self.add_btn.clicked.connect(self.add_book)
        
    def setup_inputs(self, layout):
        self.inputs = {
            'Kitap': QLineEdit(),
            'Yazar': QLineEdit(),
            'Tür': QComboBox(),
            'Başlama Tarihi': QLineEdit(),
            'Bitirme Tarihi': QLineEdit()
        }
        
        # Configure type combobox
        self.inputs['Tür'].addItems(GENRES)
        self.inputs['Tür'].setFixedWidth(200)

        for label, input_field in self.inputs.items():
            layout.addLayout(self.create_input_row(label, input_field))
            
    def add_book(self):
        if not self.validate_inputs():
            return
            
        book_data = {
            'Kitap': self.inputs['Kitap'].text(),
            'Yazar': self.inputs['Yazar'].text(),
            'Tür': self.inputs['Tür'].currentText(),
            'Başlama Tarihi': self.inputs['Başlama Tarihi'].text(),
            'Bitirme Tarihi': self.inputs['Bitirme Tarihi'].text(),
            'type': 'book'
        }
        self.data_manager.add_book(book_data)
        self.clear_inputs()