import sys
from PyQt5.QtWidgets import QApplication
from library_app import LibraryManagementApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManagementApp()
    window.show()
    sys.exit(app.exec_())
