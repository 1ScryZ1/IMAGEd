from PIL import Image, ImageDraw
import cv2


class ImageEditor:
    """
    Класс, описывающий основной функционал редактирования изображений
    """
    def __init__(self):
        """
        Инициализация
        """
        self.image = None
        self.image_backup = None

    def load_image(self, file_path):
        """
        Загрузка изображения
        :param file_path: Путь к файлу
        :return: None если ошибка
        """
        try:
            self.image = Image.open(file_path)

        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None


    @staticmethod
    def load_photo():
        """
        Метод для получения изображения с веб камеры пользователя и перехода к его редактированию
        :return: Image. если ошибка
        :return: Фотография(PIL.Image.Image)

        """
        try:
            # Включаем первую камеру
            cap = cv2.VideoCapture(0)

            # "Прогреваем" камеру, чтобы снимок не был тёмным
            for i in range(10):
                cap.read()

            # Делаем снимок
            ret, frame = cap.read()

            # Освобождаем ресурсы камеры
            cap.release()

            if ret:
                # Конвертируем изображение из формата OpenCV в формат массива numpy
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Создаем объект изображения библиотеки Pillow
                pil_image = Image.fromarray(frame_rgb)

            return pil_image


        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None

    def split_channels(self):
        """
        Разделение изображения на отдельные цветовые каналы
        :return: Список изображений
        """
        return self.image.split()

    def show_image(self):
        """
        Отображает изображение
        :return:
        """
        self.image.show()

    def _image(self):
        """
        Изменение размера изображения
        Отдельно прописано инвертирование разного количества каналов,
        иначе при работе с одноцветным изображением ошибка
        :return:
        """
        try:
            width, height = self.image.size
            size_image = Image.new(self.image.mode, (width, height))
            pixels = self.image.load()
            negative_pixels = size_image.load()
            for x in range(width):
                for y in range(height):
                    if len(pixels[x, y]) == 1:
                        # Изображение с одним каналом цвета
                        inverted_color = 255 - pixels[x, y]
                        negative_pixels[x, y] = inverted_color
                    elif len(pixels[x, y]) == 2:
                        # Изображение с двумя каналами цвета
                        r, g = pixels[x, y]
                        inverted_color = (255 - r, 255 - g)
                        negative_pixels[x, y] = inverted_color
                    elif len(pixels[x, y]) >= 3:
                        # Обычное изображение с тремя или четырьмя каналами цвета (RGB или RGBA)
                        r, g, b = pixels[x, y][:3]
                        inverted_color = (255 - r, 255 - g, 255 - b)
                        negative_pixels[x, y] = inverted_color
                    else:
                        # Неожиданное количество каналов цвета, игнорируем пиксель
                        negative_pixels[x, y] = pixels[x, y]
            self.image = size_image
        except Exception as e:
            print(str(e))

    def decrease_brightness(self, value):
        """
        Изменяет (уменьшает) яркость на заданное значение
        :param value: Значение, на которое будет уменьшена яркость
        :return:
        """

        if value > 255:
            return None

        pixels = self.image.load()
        width, height = self.image.size

        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                new_pixel = tuple(max(0, channel - value) for channel in pixel)
                pixels[x, y] = new_pixel

    def draw_circle(self, center_x, center_y, radius):
        """
        Добавляет круг на изображение
        :param center_x: X-координата центра круга
        :param center_y: Y-координата центра круга
        :param radius: Радиус круга
        :return:
        """
        draw = ImageDraw.Draw(self.image)
        color = (255, 0, 0)  # Красный цвет (RGB формат)
        outline_width = 2  # Толщина контура

        top_left = (center_x - radius, center_y - radius)
        bottom_right = (center_x + radius, center_y + radius)
        draw.ellipse([top_left, bottom_right], outline=color, width=outline_width)

    def save_image(self, file_path):
        """
        Сохраняет изображение
        :param file_path: путь к файлу
        :return:
        """

        self.image.save(file_path)