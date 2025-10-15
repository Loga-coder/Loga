import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from image_processor import ImageProcessor
from image_utils import ImageUtils


class MainWindow:
    """Главное окно приложения"""

    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений")
        self.root.geometry("900x600")

        self.current_image_path = None
        self.original_image = None
        self.processed_image = None

        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_file_panel(main_frame)
        self.create_preview_panel(main_frame)
        self.create_operations_panel(main_frame)
        self.create_control_buttons(main_frame)

    def create_file_panel(self, parent):
        """Панель загрузки файлов"""
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(file_frame, text="Загрузить изображение",
                   command=self.load_image).pack(side=tk.LEFT)

        self.file_label = ttk.Label(file_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))

    def create_preview_panel(self, parent):
        """Панель предпросмотра"""
        preview_frame = ttk.LabelFrame(parent, text="Предпросмотр")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.original_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.original_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.processed_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.processed_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    def create_operations_panel(self, parent):
        """Панель операций"""
        operations_frame = ttk.LabelFrame(parent, text="Операции")
        operations_frame.pack(fill=tk.X, pady=(0, 10))

        self.create_resize_section(operations_frame)
        self.create_rotate_section(operations_frame)

    def create_resize_section(self, parent):
        """Секция изменения размера"""
        resize_frame = ttk.Frame(parent)
        resize_frame.pack(fill=tk.X, pady=5)

        ttk.Label(resize_frame, text="Ширина:").pack(side=tk.LEFT)
        self.width_var = tk.StringVar()
        ttk.Entry(resize_frame, textvariable=self.width_var, width=8).pack(side=tk.LEFT, padx=(5, 15))

        ttk.Label(resize_frame, text="Высота:").pack(side=tk.LEFT)
        self.height_var = tk.StringVar()
        ttk.Entry(resize_frame, textvariable=self.height_var, width=8).pack(side=tk.LEFT, padx=(5, 15))

        self.keep_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(resize_frame, text="Сохранять пропорции",
                        variable=self.keep_ratio_var).pack(side=tk.LEFT, padx=(0, 15))

        ttk.Button(resize_frame, text="Изменить размер",
                   command=self.apply_resize).pack(side=tk.LEFT)

    def create_rotate_section(self, parent):
        """Секция поворота"""
        rotate_frame = ttk.Frame(parent)
        rotate_frame.pack(fill=tk.X, pady=5)

        ttk.Button(rotate_frame, text="Поворот 90°",
                   command=lambda: self.apply_rotate(90)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(rotate_frame, text="Поворот 180°",
                   command=lambda: self.apply_rotate(180)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(rotate_frame, text="Поворот 270°",
                   command=lambda: self.apply_rotate(270)).pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(rotate_frame, text="Произвольный угол:").pack(side=tk.LEFT)
        self.angle_var = tk.StringVar()
        ttk.Entry(rotate_frame, textvariable=self.angle_var, width=8).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(rotate_frame, text="Применить",
                   command=self.apply_custom_rotate).pack(side=tk.LEFT)

    def create_control_buttons(self, parent):
        """Кнопки управления"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)

        ttk.Button(button_frame, text="Сохранить",
                   command=self.save_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Сбросить",
                   command=self.reset_image).pack(side=tk.LEFT)

    def load_image(self):
        """Загрузка изображения"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )

        if file_path:
            if not ImageUtils.is_supported_format(file_path):
                messagebox.showerror("Ошибка", "Неподдерживаемый формат файла")
                return

            self.current_image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))

            try:
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                self.display_images()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {str(e)}")

    def display_images(self):
        """Отображение изображений"""
        if self.original_image:
            preview_original = self.scale_for_preview(self.original_image)
            preview_processed = self.scale_for_preview(self.processed_image)

            self.original_photo = ImageTk.PhotoImage(preview_original)
            self.processed_photo = ImageTk.PhotoImage(preview_processed)

            self.original_canvas.delete("all")
            self.processed_canvas.delete("all")

            self.original_canvas.create_image(200, 150, image=self.original_photo)
            self.processed_canvas.create_image(200, 150, image=self.processed_photo)

    def scale_for_preview(self, image):
        """Масштабирование для предпросмотра"""
        width, height = image.size
        max_size = 400

        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return image

    def apply_resize(self):
        """Изменение размера"""
        if not self.current_image_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите изображение")
            return

        try:
            width = int(self.width_var.get()) if self.width_var.get() else None
            height = int(self.height_var.get()) if self.height_var.get() else None

            self.processed_image = ImageProcessor.resize_image(
                self.current_image_path, width, height, self.keep_ratio_var.get()
            )
            self.display_images()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа для размеров")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def apply_rotate(self, angle):
        """Поворот изображения"""
        if not self.current_image_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите изображение")
            return

        try:
            self.processed_image = ImageProcessor.rotate_image(self.current_image_path, angle)
            self.display_images()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def apply_custom_rotate(self):
        """Поворот на произвольный угол"""
        if not self.current_image_path:
            return

        try:
            angle = float(self.angle_var.get())
            self.apply_rotate(angle)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для угла")

    def save_image(self):
        """Сохранение изображения"""
        if not self.processed_image:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
        )

        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Успех", "Изображение сохранено")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def reset_image(self):
        """Сброс к оригиналу"""
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_images()