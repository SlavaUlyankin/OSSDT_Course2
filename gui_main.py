"""
Графический пользовательский интерфейс для приложения LSB Steganography.
Реализован на Tkinter.
Автор: Ульянкин В.И.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from lsb_encoder import LSBEncoder
from lsb_decoder import LSBDecoder
from metrics import ImageQualityMetrics


class SteganographyGUI:
   

    def __init__(self, root):
        
        self.root = root
        self.root.title("LSB Steganography Application")
        self.root.geometry("800x650")
        self.root.resizable(True, True)

        # Переменные для хранения путей
        self.container_image_path = tk.StringVar()
        self.stego_image_path = tk.StringVar()

        # Создание системы вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Вкладка встраивания
        self.embed_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.embed_frame, text='Встраивание')
        self._create_embed_tab()

        # Вкладка извлечения
        self.extract_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extract_frame, text='Извлечение')
        self._create_extract_tab()

        # Вкладка информации
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text='О программе')
        self._create_info_tab()

    def _create_embed_tab(self):
        #"""Создание интерфейса вкладки встраивания."""
        # Кадр для выбора изображения
        select_frame = ttk.LabelFrame(self.embed_frame, text="Выбор изображения-контейнера")
        select_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(select_frame, text="Выбрать изображение (PNG/BMP)",
                   command=self.select_container_image).pack(side='left', padx=5)

        self.container_label = ttk.Label(select_frame, text="Не выбрано")
        self.container_label.pack(side='left', padx=20)

        # Информация о контейнере
        info_frame = ttk.LabelFrame(self.embed_frame, text="Информация о контейнере")
        info_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(info_frame, text="Размер:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.container_size_label = ttk.Label(info_frame, text="-")
        self.container_size_label.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Label(info_frame, text="Вместимость:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.container_capacity_label = ttk.Label(info_frame, text="-")
        self.container_capacity_label.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # Поле ввода текста
        msg_frame = ttk.LabelFrame(self.embed_frame, text="Сообщение для встраивания")
        msg_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.embed_text = tk.Text(msg_frame, height=6, width=80)
        self.embed_text.pack(fill='both', expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.embed_text)
        scrollbar.pack(side='right', fill='y')
        self.embed_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.embed_text.yview)

        # Кнопка встраивания
        ttk.Button(self.embed_frame, text="Встроить сообщение",
                   command=self.embed_message).pack(pady=10)

        # Статус
        self.embed_status = ttk.Label(self.embed_frame, text="", foreground="blue")
        self.embed_status.pack()

    def _create_extract_tab(self):
        #"""Создание интерфейса вкладки извлечения."""
        # Кадр для выбора стего-изображения
        select_frame = ttk.LabelFrame(self.extract_frame, text="Выбор стего-изображения")
        select_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(select_frame, text="Выбрать стего-изображение",
                   command=self.select_stego_image).pack(side='left', padx=5)

        self.stego_label = ttk.Label(select_frame, text="Не выбрано")
        self.stego_label.pack(side='left', padx=20)

        # Кнопка извлечения
        ttk.Button(self.extract_frame, text="Извлечь сообщение",
                   command=self.extract_message).pack(pady=10)

        # Поле вывода текста
        msg_frame = ttk.LabelFrame(self.extract_frame, text="Извлеченное сообщение")
        msg_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.extract_text = tk.Text(msg_frame, height=8, width=80, state='disabled')
        self.extract_text.pack(fill='both', expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.extract_text)
        scrollbar.pack(side='right', fill='y')
        self.extract_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.extract_text.yview)

        # Кнопка копирования
        ttk.Button(self.extract_frame, text="Копировать в буфер обмена",
                   command=self.copy_to_clipboard).pack(pady=10)

        # Статус
        self.extract_status = ttk.Label(self.extract_frame, text="", foreground="blue")
        self.extract_status.pack()

    def _create_info_tab(self):
        #"""Создание интерфейса вкладки информации."""
        info_text = tk.Text(self.info_frame, wrap='word')
        info_text.pack(fill='both', expand=True, padx=10, pady=10)

        info_content = """LSB STEGANOGRAPHY APPLICATION
Версия 1.0
Автор: Ульянкин Вячеслав Игоревич

ОПИСАНИЕ
Приложение для встраивания и извлечения текстовой информации в цифровые 
изображения методом LSB (Least Significant Bit).

ОСОБЕННОСТИ
• Встраивание текстовых сообщений в изображения PNG и BMP
• Извлечение встроенной информации из стего-изображений
• Расчет метрик качества (PSNR, MSE, SSIM)
• Графический пользовательский интерфейс на Tkinter

ТРЕБОВАНИЯ
• Python 3.10+
• Pillow - обработка изображений
• NumPy - работа с массивами
• OpenCV - расчет метрик
• scikit-image - индекс структурного сходства

ИСПОЛЬЗОВАНИЕ
1. Вкладка "Встраивание": выберите изображение, введите текст, нажмите встраивание
2. Вкладка "Извлечение": выберите стего-изображение, нажмите извлечение
3. Вкладка "О программе": информация о приложении

ЛИЦЕНЗИЯ
Открытый исходный код (GPL)
"""

        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')

    def select_container_image(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.bmp"), ("PNG", "*.png"), ("BMP", "*.bmp")]
        )

        if file_path:
            try:
                self.container_image_path.set(file_path)
                encoder = LSBEncoder(file_path)
                info = encoder.get_image_info()

                self.container_label.config(text=os.path.basename(file_path))
                self.container_size_label.config(text=f"{info['width']}×{info['height']}")
                self.container_capacity_label.config(text=f"{info['capacity']} символов")
                self.embed_status.config(text="", foreground="blue")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке изображения: {e}")

    def select_stego_image(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.bmp"), ("PNG", "*.png"), ("BMP", "*.bmp")]
        )

        if file_path:
            self.stego_image_path.set(file_path)
            self.stego_label.config(text=os.path.basename(file_path))
            self.extract_status.config(text="")

    def embed_message(self):
        
        if not self.container_image_path.get():
            messagebox.showwarning("Внимание", "Выберите изображение-контейнер")
            return

        message = self.embed_text.get('1.0', 'end-1c')

        if not message:
            messagebox.showwarning("Внимание", "Введите сообщение")
            return

        try:
            self.embed_status.config(text="Обработка...", foreground="blue")
            self.root.update()

            output_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )

            if output_path:
                encoder = LSBEncoder(self.container_image_path.get())
                encoder.embed_data(message, output_path)

                # Расчет метрик качества
                metrics = ImageQualityMetrics.get_full_report(
                    self.container_image_path.get(), output_path
                )

                status_msg = f"Встраивание успешно! MSE: {metrics['MSE']}, PSNR: {metrics['PSNR']} dB, " \
                            f"SSIM: {metrics['SSIM']}, Качество: {metrics['Quality']}"
                self.embed_status.config(text=status_msg, foreground="green")
                messagebox.showinfo("Успех", status_msg)
        except Exception as e:
            self.embed_status.config(text=f"Ошибка: {e}", foreground="red")
            messagebox.showerror("Ошибка", f"Ошибка при встраивании: {e}")

    def extract_message(self):
        
        if not self.stego_image_path.get():
            messagebox.showwarning("Внимание", "Выберите стего-изображение")
            return

        try:
            self.extract_status.config(text="Обработка...", foreground="blue")
            self.root.update()

            decoder = LSBDecoder(self.stego_image_path.get())
            extracted_message = decoder.extract_data()

            self.extract_text.config(state='normal')
            self.extract_text.delete('1.0', 'end')
            self.extract_text.insert('1.0', extracted_message)
            self.extract_text.config(state='disabled')

            self.extract_status.config(text="Извлечение завершено успешно", foreground="green")
        except Exception as e:
            self.extract_status.config(text=f"Ошибка: {e}", foreground="red")
            messagebox.showerror("Ошибка", f"Ошибка при извлечении: {e}")

    def copy_to_clipboard(self):
        
        text = self.extract_text.get('1.0', 'end-1c')

        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Успех", "Текст скопирован в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Нечего копировать")


def main():
    
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()