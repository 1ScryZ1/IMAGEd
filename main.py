from PyQt5.QtWidgets import QApplication
from GUI import ImageEdWindow

if __name__ == "__main__":
    app = QApplication([])
    window = ImageEdWindow()
    window.show()
    app.exec_()