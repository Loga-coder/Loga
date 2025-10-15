import os


class ImageUtils:
    """Вспомогательные утилиты для работы с изображениями"""

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

    @staticmethod
    def is_supported_format(file_path):
        """Проверка поддерживаемого формата"""
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ImageUtils.SUPPORTED_FORMATS

    @staticmethod
    def get_image_info(image_path):
        """Получение информации об изображении"""
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'size': os.path.getsize(image_path)
                }
        except Exception as e:
            raise Exception(f"Ошибка получения информации: {str(e)}")