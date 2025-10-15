from PIL import Image

class ImageProcessor:
    def resize_image(image_path, new_width=None, new_height=None, keep_aspect_ratio=True):
        "Изменение размера изображения"
        try:
            with Image.open(image_path) as img:
                original_width, original_height = img.size

                if keep_aspect_ratio:
                    if new_width and new_height:
                        ratio = min(new_width / original_width, new_height / original_height)
                        new_width = int(original_width * ratio)
                        new_height = int(original_height * ratio)
                    elif new_width:
                        ratio = new_width / original_width
                        new_height = int(original_height * ratio)
                    elif new_height:
                        ratio = new_height / original_height
                        new_width = int(original_width * ratio)

                return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        except Exception as e:
            raise Exception(f"Ошибка изменения размера: {str(e)}")


    def rotate_image(image_path, angle):
        """Поворот изображения"""
        try:
            with Image.open(image_path) as img:
                return img.rotate(-angle, expand=True)
        except Exception as e:
            raise Exception(f"Ошибка поворота: {str(e)}")