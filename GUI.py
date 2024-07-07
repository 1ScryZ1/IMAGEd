from PyQt5.QtWidgets import QMessageBox, QMainWindow, \
                            QLabel, QPushButton, QVBoxLayout, \
                            QWidget, QLineEdit, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap, QImage, QIntValidator
from PyQt5.QtCore import Qt
from IMAGEd import ImageEditor
from IMAGEd import Image


def convert_pil_to_qimage(pil_image):
    """
    Конвертация Pillow-изображения в QImage
    :param pil_image: Pillow-изображение
    :return: QImage object
    """
    image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
    qimage = QImage(image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
    return qimage


class ImageEditorWindow(QMainWindow):
    """
    Класс, описывающий поведение графического интерфейса пользователя (GUI)
    GUI работает на библиотеке PyQT
    """
    def __init__(self):
        """
        Инициализация
        """
        super().__init__()

        self.setWindowTitle("ImageEd")
        self.image_editor = ImageEditor()
        self.is_image_loaded = False

        self.setup_ui()

    def setup_ui(self):
        """
        Настройка интерфейса
        :return:
        """
        main_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("Загрузите изображение")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.load_button = QPushButton("Загрузить изображение")
        # При нажатии на кнопку сработает метод load_image
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        self.photo_button = QPushButton("Сделать фотографию")
        # При нажатии на кнопку сработает метод load_photo
        self.photo_button.clicked.connect(self.load_photo)
        layout.addWidget(self.photo_button)

        self.channel_combo = QComboBox()
        self.channel_combo.addItem("Все каналы (RGB)")
        self.channel_combo.addItem("Красный (R)")
        self.channel_combo.addItem("Зеленый (G)")
        self.channel_combo.addItem("Синий (B)")
        # Привязываем к боксу метод update_image_channel
        self.channel_combo.currentIndexChanged.connect(self.update_image_channel)
        self.channel_combo.setEnabled(False)
        layout.addWidget(self.channel_combo)

        self.size_button = QPushButton("Изменить размер изображения")
        self.size_button.clicked.connect(self.resize_image)
        self.size_button.setEnabled(False)
        layout.addWidget(self.size_button)

        self.brightness_button = QPushButton("Понизить яркость изображения")
        # Привязываем метод decrease_brightness к кнопке
        self.brightness_button.clicked.connect(self.decrease_brightness)
        self.brightness_button.setEnabled(False)
        layout.addWidget(self.brightness_button)

        self.circle_button = QPushButton("Нарисовать круг на изображении")
        # Привязываем к кнопке метод draw_circle
        self.circle_button.clicked.connect(self.draw_circle)
        self.circle_button.setEnabled(False)
        layout.addWidget(self.circle_button)

        self.brightness_value_input = QLineEdit()
        self.brightness_value_input.setPlaceholderText("Значение, на которое будет понижена яркость (от 0 до 255)")
        # Привязываем метод check_inputs к QLine объекту
        self.brightness_value_input.textChanged.connect(self.check_inputs)
        self.brightness_value_input.setValidator(QIntValidator(0, 255, self))
        layout.addWidget(self.brightness_value_input)

        self.circle_x_input = QLineEdit()
        self.circle_x_input.setPlaceholderText("X относительно центра круга")
        # Привязываем метод check_inputs к QLine объекту
        self.circle_x_input.textChanged.connect(self.check_inputs)
        self.circle_x_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.circle_x_input)

        self.circle_y_input = QLineEdit()
        self.circle_y_input.setPlaceholderText("Y относительно центра круга")
        # Привязываем метод check_inputs к QLine объекту
        self.circle_y_input.textChanged.connect(self.check_inputs)
        self.circle_y_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.circle_y_input)

        self.circle_radius_input = QLineEdit()
        self.circle_radius_input.setPlaceholderText("Радиус круга")
        # Привязываем метод check_inputs к QLine объекту
        self.circle_radius_input.textChanged.connect(self.check_inputs)
        self.circle_radius_input.setValidator(QIntValidator(0, 9999, self))
        layout.addWidget(self.circle_radius_input)

        self.save_button = QPushButton("Сохранить изображение")
        # Привязываем метод save_image к кнопке
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setFixedWidth(1000)
        self.setFixedHeight(800)

    def load_image(self):
        """
        метод для загрузки для загрузки изображения с устройства
        :return:
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg)")

        if file_path:
            self.image_editor.load_image(file_path)
            self.is_image_loaded = True
            self.label.setText("Изображение успешно загружено")
            self.update_buttons_state()
            self.show_image()

    def load_photo(self):
        photo = self.image_editor.load_photo()

        if photo is None:
            error = QMessageBox()
            error.setWindowTitle("Ошибка!")
            error.setText("Произошла ошибка при работе с вебкамерой!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.setInformativeText("Проверьте, подключена ли камера к компьютеру.")
            error.exec_()
        else:
            self.image_editor.image = photo
            self.is_image_loaded = True
            self.label.setText("Фотография сделана успешно")
            self.update_buttons_state()
            self.show_image()



    def update_image_channel(self):
        """
        Обновляет отображаемый канал изображения
        :return:
        """
        channel = self.channel_combo.currentIndex()
        if channel == 0:
            self.show_image()
        else:
            self.show_image_channel(channel)

    def show_image_channel(self, channel):
        """
        Размещение выбранного канала изображения в окне GUI
        :param channel: Индекс выбранного канала
        :return:
        """
        try:
            if self.image_editor.image:
                image = self.image_editor.image
                red, green, blue = image.split()
                empty_pixels = red.point(lambda _:0)
                red_img = Image.merge("RGB", (red, empty_pixels,
                                                         empty_pixels))
                green_img = Image.merge("RGB", (empty_pixels, green,
                                                         empty_pixels))
                blue_img = Image.merge("RGB", (empty_pixels, empty_pixels,
                                                       blue))
                channel_image = [red_img, green_img, blue_img][channel - 1]
                qimage = convert_pil_to_qimage(channel_image)
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
        :return:
        """
        decrease_value = int(self.brightness_value_input.text())
        self.image_editor.decrease_brightness(decrease_value)
        self.label.setText("Яркость понижена")
        self.update_buttons_state()
        self.show_image()

    def draw_circle(self):
        """
        Метод для круга на изображении
        :return:
        """
        center_x = int(self.circle_x_input.text())
        center_y = int(self.circle_y_input.text())
        radius = int(self.circle_radius_input.text())
        self.image_editor.draw_circle(center_x, center_y, radius)
        self.label.setText("Круг нарисован")
        self.update_buttons_state()
        self.show_image()

    def save_image(self):
        """
        Метод для сохранения изображения
        :return:
        """
        try:

            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "Images (*.png *.jpg *.jpeg)")

            if file_path:
                self.image_editor.save_image(file_path)
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
        Проверяем поля ввода, если нужные поля активны, то кнопки активируются
        :return:
        """
        brightness = self.brightness_value_input.text()
        circle_x = self.circle_x_input.text()
        circle_y = self.circle_y_input.text()
        circle_radius = self.circle_radius_input.text()

        self.channel_combo.setEnabled(self.is_image_loaded)
        self.size_button.setEnabled(self.is_image_loaded)
        self.brightness_button.setEnabled(bool(brightness) and self.is_image_loaded)
        self.circle_button.setEnabled(bool(circle_x)
                                      and bool(circle_y)
                                      and bool(circle_radius)
                                      and self.is_image_loaded)
        self.save_button.setEnabled(self.is_image_loaded)

    def update_buttons_state(self):
        """
        Обновление состояния кнопок
        :return:
        """
        self.check_inputs()
        self.brightness_value_input.clear()
        self.circle_x_input.clear()
        self.circle_y_input.clear()
        self.circle_radius_input.clear()

    def show_image(self):
        """
        Размещение изображения в окне GUI
        :return:
        """
        if self.image_editor.image:
            image = self.image_editor.image
            qimage = convert_pil_to_qimage(image)
            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled_pixmap)
        else:
            self.label.clear()