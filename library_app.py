from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from components.book_section import BookSection
from components.article_section import ArticleSection
from components.magazine_section import MagazineSection
from components.table_widget import TableWidget
from components.button_panel import ButtonPanel
from data_manager import DataManager

class LibraryManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kütüphane Yönetim Sistemi")
        self.setMinimumSize(1200, 800)  # Set minimum window size
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Setup UI
        self.setup_ui()
        
        # Load initial data
        self.data_manager.load_data()
        
    def setup_ui(self):
        # Create central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout with fixed spacing
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Create sections container with fixed height
        sections_container = QWidget()
        sections_container.setFixedHeight(350)
        sections_layout = QHBoxLayout(sections_container)
        sections_layout.setSpacing(20)
        sections_layout.setContentsMargins(0, 0, 0, 0)

        # Create sections
        self.book_section = BookSection(self.data_manager)
        self.article_section = ArticleSection(self.data_manager)
        self.magazine_section = MagazineSection(self.data_manager)
        
        # Add sections to container
        sections_layout.addWidget(self.book_section)
        sections_layout.addWidget(self.article_section)
        sections_layout.addWidget(self.magazine_section)
        
        # Create table widget
        self.table_widget = TableWidget(self.data_manager)
        
        # Create button panel
        self.button_panel = ButtonPanel(
            self.data_manager,
            self.table_widget,
            self.book_section,
            self.article_section,
            self.magazine_section
        )
        
        # Add widgets to main layout
        main_layout.addWidget(sections_container)
        main_layout.addWidget(self.button_panel)
        main_layout.addWidget(self.table_widget)