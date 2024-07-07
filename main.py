from PyQt5.QtWidgets import QApplication
from GUI import ImageEditorWindow

if __name__ == "__main__":
    app = QApplication([])
    window = ImageEditorWindow()
    window.show()
    app.exec_()