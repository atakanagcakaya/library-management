from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QWidget
from .base_section import BaseSection

class MagazineSection(BaseSection):
    def __init__(self, data_manager):
        super().__init__("Dergi", data_manager)
        self.add_btn.clicked.connect(self.add_magazine)
        
    def setup_inputs(self, layout):
        self.inputs = {
            'Dergi': QLineEdit(),
            'Sayı': QLineEdit(),
            'Cilt': QLineEdit(),
            'Tarih': QLineEdit(),
            'Başlama Tarihi': QLineEdit(),
            'Bitirme Tarihi': QLineEdit()
        }
        
        # Create special layout for Sayı and Cilt
        sayi_cilt_layout = QHBoxLayout()
        sayi_cilt_layout.addLayout(self.create_input_row('Sayı', self.inputs['Sayı']))
        sayi_cilt_layout.addLayout(self.create_input_row('Cilt', self.inputs['Cilt']))
        
        # Add other inputs
        layout.addLayout(self.create_input_row('Dergi', self.inputs['Dergi']))
        layout.addLayout(sayi_cilt_layout)
        layout.addLayout(self.create_input_row('Tarih', self.inputs['Tarih']))
        layout.addLayout(self.create_input_row('Başlama Tarihi', self.inputs['Başlama Tarihi']))
        layout.addLayout(self.create_input_row('Bitirme Tarihi', self.inputs['Bitirme Tarihi']))
            
    def add_magazine(self):
        if not self.validate_inputs():
            return
            
        magazine_data = {key: input_field.text() for key, input_field in self.inputs.items()}
        magazine_data['type'] = 'magazine'
        self.data_manager.add_magazine(magazine_data)
        self.clear_inputs()