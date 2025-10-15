import os
from PIL import Image


class ImageUtils:
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    def __init__(self):
        pass

    def is_supported_format(self, file_path):
        "Проверка поддерживаемого формата"
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_FORMATS

    def get_image_info(self, image_path):
        "Получение информации об изображении"
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'size': os.path.getsize(image_path)
                }
        except Exception as e:
            raise Exception(f"Ошибка получения информации: {str(e)}")