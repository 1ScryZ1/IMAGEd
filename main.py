from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication
from GUI import ImageEdWindow

if __name__ == "__main__":
    app = QApplication([])
    window = ImageEdWindow()
    window.show()
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.lightGray)
    palette.setColor(QPalette.WindowText, Qt.darkBlue)
    palette.setColor(QPalette.ButtonText, Qt.darkCyan)
    app.setPalette(palette)
    app.exec_()