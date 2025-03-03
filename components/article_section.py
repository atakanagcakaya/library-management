from PyQt5.QtWidgets import QLineEdit, QComboBox, QLabel
from .base_section import BaseSection
from src.constants import GENRES, add_genre

class ArticleSection(BaseSection):
    def __init__(self, data_manager):
        super().__init__("Makale", data_manager)
        self.add_btn.clicked.connect(self.add_article)
        
    def setup_inputs(self, layout):
        self.inputs = {
            'Makale': QLineEdit(),
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
            
    def add_article(self):
        if not self.validate_inputs():
            return
            
        article_data = {
            'Makale': self.inputs['Makale'].text(),
            'Yazar': self.inputs['Yazar'].text(),
            'Tür': self.inputs['Tür'].currentText(),
            'Başlama Tarihi': self.inputs['Başlama Tarihi'].text(),
            'Bitirme Tarihi': self.inputs['Bitirme Tarihi'].text(),
            'type': 'article'
        }
        self.data_manager.add_article(article_data)
        self.clear_inputs()