import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os


class ImageProcessor:
    def resize_image(self, image, width, height, keep_ratio=True):
        if not (width or height): return image
        w, h = image.size
        if keep_ratio:
            if not width:
                width = int(w * height / h)
            elif not height:
                height = int(h * width / w)
            else:
                ratio = min(width / w, height / h)
                width, height = int(w * ratio), int(h * ratio)
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def rotate_image(self, image, angle):
        return image.rotate(angle, expand=True)


class ImageUtils:
    def is_supported_format(self, file_path):
        return os.path.splitext(file_path)[1].lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений")
        self.root.geometry("900x600")
        self.current_image_path = None
        self.original_image = None
        self.processed_image = None
        self.image_processor = ImageProcessor()
        self.image_utils = ImageUtils()
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(file_frame, text="Загрузить изображение", command=self.load_image).pack(side=tk.LEFT)
        self.file_label = ttk.Label(file_frame, text="Файл не выбран")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))

        preview_frame = ttk.LabelFrame(main_frame, text="Предпросмотр")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.original_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.original_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.processed_canvas = tk.Canvas(preview_frame, bg='white', height=300)
        self.processed_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        operations_frame = ttk.LabelFrame(main_frame, text="Операции")
        operations_frame.pack(fill=tk.X, pady=(0, 10))

        resize_frame = ttk.Frame(operations_frame)
        resize_frame.pack(fill=tk.X, pady=5)
        ttk.Label(resize_frame, text="Ширина:").pack(side=tk.LEFT)
        self.width_var = tk.StringVar()
        ttk.Entry(resize_frame, textvariable=self.width_var, width=8).pack(side=tk.LEFT, padx=(5, 15))
        ttk.Label(resize_frame, text="Высота:").pack(side=tk.LEFT)
        self.height_var = tk.StringVar()
        ttk.Entry(resize_frame, textvariable=self.height_var, width=8).pack(side=tk.LEFT, padx=(5, 15))
        self.keep_ratio_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(resize_frame, text="Сохранять пропорции", variable=self.keep_ratio_var).pack(side=tk.LEFT,
                                                                                                     padx=(0, 15))
        ttk.Button(resize_frame, text="Изменить размер", command=self.apply_resize).pack(side=tk.LEFT)

        rotate_frame = ttk.Frame(operations_frame)
        rotate_frame.pack(fill=tk.X, pady=5)
        for angle, text in [(90, "90°"), (180, "180°"), (270, "270°")]:
            ttk.Button(rotate_frame, text=f"Поворот {text}", command=lambda a=angle: self.apply_rotate(a)).pack(
                side=tk.LEFT, padx=(0, 5))
        ttk.Label(rotate_frame, text="Произвольный угол:").pack(side=tk.LEFT)
        self.angle_var = tk.StringVar()
        ttk.Entry(rotate_frame, textvariable=self.angle_var, width=8).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(rotate_frame, text="Применить", command=self.apply_custom_rotate).pack(side=tk.LEFT)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Сохранить", command=self.save_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Сбросить", command=self.reset_image).pack(side=tk.LEFT)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path and self.image_utils.is_supported_format(file_path):
            self.current_image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            try:
                self.original_image = Image.open(file_path)
                self.processed_image = self.original_image.copy()
                self.display_images()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {str(e)}")

    def display_images(self):
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
        w, h = image.size
        max_size = 400
        if w > max_size or h > max_size:
            ratio = min(max_size / w, max_size / h)
            return image.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
        return image

    def apply_resize(self):
        if not self.processed_image:
            messagebox.showwarning("Ошибка", "Сначала загрузите изображение")
            return
        try:
            width = int(self.width_var.get()) if self.width_var.get() else None
            height = int(self.height_var.get()) if self.height_var.get() else None
            self.processed_image = self.image_processor.resize_image(self.processed_image, width, height,
                                                                     self.keep_ratio_var.get())
            self.display_images()
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числа для размеров")

    def apply_rotate(self, angle):
        if self.processed_image:
            try:
                self.processed_image = self.image_processor.rotate_image(self.processed_image, angle)
                self.display_images()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
    
    def apply_custom_rotate(self):
        if self.processed_image:
            try:
                self.apply_rotate(float(self.angle_var.get()))
            except ValueError:
                messagebox.showerror("Ошибка", "Введите число для угла")

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if file_path:
                try:
                    self.processed_image.save(file_path)
                    messagebox.showinfo("Успех", "Изображение сохранено")
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.display_images()
