from PIL import Image
import numpy as np
import os


class LSBDecoder:
    
    def __init__(self, stego_image_path):
        
        if not os.path.exists(stego_image_path):
            raise FileNotFoundError(f"Файл {stego_image_path} не найден")

        try:
            self.image = Image.open(stego_image_path)
            # Конвертируем в RGB для единообразного формата
            self.image = self.image.convert('RGB')
            self.pixels = np.array(self.image)
            self.height, self.width = self.pixels.shape[:2]
        except Exception as e:
            raise Exception(f"Ошибка при загрузке изображения: {str(e)}")

    def extract_data(self):
        
        try:
            # Создание плоского представления массива пикселей
            pixels_flat = self.pixels.reshape(-1)

            # Извлечение младшего бита из каждого элемента
            # Операция & 1 извлекает последний бит (если 1, то значение нечетное)
            binary_message = ''.join(str(pixel & 1) for pixel in pixels_flat)

            # Преобразование бинарной последовательности в текст
            message = ''
            for i in range(0, len(binary_message), 8):
                # Взятие группы из 8 бит (одного байта)
                byte = binary_message[i:i+8]

                if len(byte) == 8:
                    # Преобразование двоичного кода в символ ASCII
                    try:
                        char = chr(int(byte, 2))
                        message += char
                    except ValueError:
                        # Пропуск некорректных кодов
                        continue

                    # Проверка на маркер конца
                    if message.endswith('[END]'):
                        # Возврат сообщения без маркера конца
                        return message[:-5]

            # Если маркер конца не найден
            if message:
                return message
            else:
                return ""

        except Exception as e:
            raise Exception(f"Ошибка при извлечении: {str(e)}")

    def get_image_info(self):
        
        return {
            'width': self.width,
            'height': self.height,
            'size': f"{self.width}×{self.height}",
            'total_pixels': self.height * self.width
        }


# Пример использования (если запуск как отдельный скрипт)
if __name__ == "__main__":
    try:
        # Пример извлечения
        decoder = LSBDecoder("stego_image.png")
        print("Информация об изображении:", decoder.get_image_info())

        extracted_message = decoder.extract_data()
        print("Извлеченное сообщение:", extracted_message)
    except Exception as e:
        print(f"Ошибка: {e}")