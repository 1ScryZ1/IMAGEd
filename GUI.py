from PyQt5.QtWidgets import QMessageBox, QMainWindow, \
                            QLabel, QPushButton, QVBoxLayout, \
                            QWidget, QLineEdit, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QImage, QIntValidator
from PyQt5.QtCore import Qt
from IMAGEd import ImageEd


def converterpillow(pil_image):
    """
    Конвертация Pillow-изображения в QImage
    """
    image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
    qimage = QImage(image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
    return qimage


class ImageEdWindow(QMainWindow):
    """
    Класс, описывающий поведение графического интерфейса пользователя (GUI)
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IMAGEd")
        self.imaged = ImageEd()
        self.imageloader = False

        self.UIsetup()

    def UIsetup(self):
        """
        Настройка интерфейса
        """
        mwidget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("Загрузите изображение")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.btn_load = QPushButton("Загрузить изображение")
        self.btn_load.clicked.connect(self.load_image)
        layout.addWidget(self.btn_load)

        self.btn_photo = QPushButton("Сделать фотографию")
        self.btn_photo.clicked.connect(self.load_photo)
        layout.addWidget(self.btn_photo)

        self.channel_RGB = QComboBox()
        self.channel_RGB.addItem("Все каналы (RGB)")
        self.channel_RGB.addItem("Красный (R)")
        self.channel_RGB.addItem("Зеленый (G)")
        self.channel_RGB.addItem("Синий (B)")
        self.channel_RGB.currentIndexChanged.connect(self.update_image_channel)
        self.channel_RGB.setEnabled(False)
        layout.addWidget(self.channel_RGB)

        self.btn_resize = QPushButton("Изменить размер изображения")
        self.btn_resize.clicked.connect(self.resize_image)
        self.btn_resize.setEnabled(False)
        layout.addWidget(self.btn_resize)

        self.btn_brightness = QPushButton("Понизить яркость изображения")
        self.btn_brightness.clicked.connect(self.decrease_brightness)
        self.btn_brightness.setEnabled(False)
        layout.addWidget(self.btn_brightness)

        self.btn_circle = QPushButton("Нарисовать круг на изображении")
        self.btn_circle.clicked.connect(self.draw_circle)
        self.btn_circle.setEnabled(False)
        layout.addWidget(self.btn_circle)

        self.widthvalue_input = QLineEdit()
        self.widthvalue_input.setPlaceholderText("Новая ширина изображения")
        self.widthvalue_input.textChanged.connect(self.check_inputs)
        self.widthvalue_input.setValidator(QIntValidator(0, 999, self))
        layout.addWidget(self.widthvalue_input)

        self.heightvalue_input = QLineEdit()
        self.heightvalue_input.setPlaceholderText("Новая высота изображения")
        self.heightvalue_input.textChanged.connect(self.check_inputs)
        self.heightvalue_input.setValidator(QIntValidator(0, 999, self))
        layout.addWidget(self.heightvalue_input)

        self.brightness_value_input = QLineEdit()
        self.brightness_value_input.setPlaceholderText("Значение, на которое будет понижена яркость изображения")
        self.brightness_value_input.textChanged.connect(self.check_inputs)
        self.brightness_value_input.setValidator(QIntValidator(0, 255, self))
        layout.addWidget(self.brightness_value_input)

        self.circle_x_input = QLineEdit()
        self.circle_x_input.setPlaceholderText("Размещение по X центра круга")
        self.circle_x_input.textChanged.connect(self.check_inputs)
        self.circle_x_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.circle_x_input)

        self.circle_y_input = QLineEdit()
        self.circle_y_input.setPlaceholderText("Размещение по Y центра круга")
        self.circle_y_input.textChanged.connect(self.check_inputs)
        self.circle_y_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.circle_y_input)

        self.cirradius_input = QLineEdit()
        self.cirradius_input.setPlaceholderText("Радиус круга")
        self.cirradius_input.textChanged.connect(self.check_inputs)
        self.cirradius_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.cirradius_input)

        self.btn_save = QPushButton("Сохранить изображение")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        mwidget.setLayout(layout)
        self.setCentralWidget(mwidget)

        self.setFixedWidth(900)
        self.setFixedHeight(1200)

    def load_image(self):
        """
        Метод для загрузки для загрузки изображения с устройства
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg)")

        if file_path:
            self.imaged.load_image(file_path)
            self.imageloader = True
            self.label.setText("Изображение успешно загружено")
            self.update_buttons_state()
            self.show_image()

    def resize_image(self):
        new_width = int(self.widthvalue_input.text())
        new_height = int(self.heightvalue_input.text())
        self.imaged = self.imaged.resizer((new_width, new_height))


    def load_photo(self):
        photo = self.imaged.photoloader()

        if photo is None:
            error = QMessageBox()
            error.setWindowTitle("Ошибка!")
            error.setText("Ошибка при работе с веб-камерой!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Проверьте, подключена ли ваша веб-камера к вашему устройству")
            error.exec_()
        else:
            self.imaged.image = photo
            self.imageloader = True
            self.label.setText("Фотография сделана успешно")
            self.update_buttons_state()
            self.show_image()

    def update_image_channel(self):
        """
        Обновляет отображаемый канал изображения
        """
        channel = self.channel_RGB.currentIndex()
        if channel == 0:
            self.show_image()
        else:
            self.show_image_channel(channel)

    def show_image_channel(self, channel):
        """
        Размещение выбранного канала изображения в окне GUI
        """
        try:
            if self.imaged.image:
                channel_image = self.imaged.image_channel(channel - 1)
                qimage = converterpillow(channel_image)
                pixmap = QPixmap.fromImage(qimage)
                scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.label.setPixmap(scaled_pixmap)
            else:
                self.label.clear()
        except Exception as e:
            print(str(e))

    def decrease_brightness(self):
        """
        Метод для изменения яркости изображения
        """
        decrease_value = int(self.brightness_value_input.text())
        self.imaged.decrease_brightness(decrease_value)
        self.label.setText("Яркость успешно понижена")
        self.update_buttons_state()
        self.show_image()

    def draw_circle(self):
        """
        Метод для круга на изображении
        """
        center_x = int(self.circle_x_input.text())
        center_y = int(self.circle_y_input.text())
        radius = int(self.cirradius_input.text())
        self.imaged.draw_circle(center_x, center_y, radius)
        self.label.setText("Круг успешно нарисован")
        self.update_buttons_state()
        self.show_image()

    def save_image(self):
        """
        Метод для сохранения изображения
        """
        try:

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "Images (*.png *.jpg *.jpeg)")

            if file_path:
                self.imaged.save_image(file_path)
                self.label.setText("Изображение успешно сохранено")
        except Exception as e:
            error = QMessageBox()
            error.setWindowTitle("Ошибка!")
            error.setText("Произошла ошибка при сохранении файла!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Проверьте расширение сохраняемого файла")
            error.exec_()

    def check_inputs(self):
        """
        Метод активации и деактивации кнопок
        """
        brightness = self.brightness_value_input.text()
        circle_x = self.circle_x_input.text()
        circle_y = self.circle_y_input.text()
        circle_radius = self.cirradius_input.text()

        self.channel_RGB.setEnabled(self.imageloader)
        self.btn_load.setEnabled(self.imageloader)
        self.btn_resize.setEnabled(self.imageloader)
        self.btn_brightness.setEnabled(bool(brightness) and self.imageloader)
        self.btn_circle.setEnabled(bool(circle_x)
                                      and bool(circle_y)
                                      and bool(circle_radius)
                                      and self.imageloader)
        self.btn_save.setEnabled(self.imageloader)

    def update_buttons_state(self):
        """
        Обновление состояния кнопок
        """
        self.check_inputs()
        self.brightness_value_input.clear()
        self.circle_x_input.clear()
        self.circle_y_input.clear()
        self.cirradius_input.clear()

    def show_image(self):
        """
        Размещение изображения в окне GUI
        """
        if self.imaged.image:
            image = self.imaged.image
            qimage = converterpillow(image)
            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled_pixmap)
        else:
            self.label.clear()