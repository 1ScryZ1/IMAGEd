from PIL import Image, ImageDraw
import cv2


class ImageEd:
    """
    Класс, содержащий основной функционал редактирования изображений
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
        """
        try:
            self.image = Image.open(file_path)
            self.image = self.image.convert("RGB")

        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None


    @staticmethod
    def load_photo():
        """
        Метод для получения изображения с веб-камеры пользователя
        """
        try:
            wbcam = cv2.VideoCapture(0)

            for i in range(10):
                wbcam.read()

            ret, frame = wbcam.read()

            wbcam.release()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Создаем объект изображения библиотеки Pillow
                pil_image = Image.fromarray(frame_rgb)

            return pil_image.convert("RGB")


        except Exception as e:
            print("Ошибка при загрузке изображения:", str(e))
            return None

    def image_channel(self, channel):
        """
        Получение канала изображения
        """
        try:
            image = self.image.convert("RGB")
            red, green, blue = image.split()
            empty_pixels = red.point(lambda _: 0)
            red_merge = Image.merge("RGB", (red, empty_pixels, empty_pixels))
            green_merge = Image.merge("RGB", (empty_pixels, green, empty_pixels))
            blue_merge = Image.merge("RGB", (empty_pixels, empty_pixels, blue))
            channels_list = [red_merge, green_merge, blue_merge]
            return channels_list[channel]

        except Exception as e:
            print(str(e))

    def decrease_brightness(self, value):
        """
        Уменьшает яркость на заданное значение
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
        """

        self.image.save(file_path)