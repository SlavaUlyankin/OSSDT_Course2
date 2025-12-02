from PIL import Image
import numpy as np
import os


class LSBEncoder:
    #Класс для встраивания информации в изображение методом LSB.

    def __init__(self, image_path):
       
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Файл {image_path} не найден")

        try:
            self.image = Image.open(image_path)
            self.image = self.image.convert('RGB')
            self.pixels = np.array(self.image)
            self.height, self.width = self.pixels.shape[:2]
        except Exception as e:
            raise Exception(f"Ошибка при загрузке изображения: {str(e)}")

    def text_to_binary(self, text):
        
        binary_text = ''.join(format(ord(c), '08b') for c in text)
        return binary_text

    def binary_to_text(self, binary):
        
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text

    def calculate_capacity(self):
       
        total_bits = self.height * self.width * 3  
        total_bytes = total_bits // 8
        capacity = max(0, total_bytes - 10)
        return capacity

    def embed_data(self, message, output_path='stego_image.png'):
      
        capacity = self.calculate_capacity()
        if len(message) > capacity:
            raise ValueError(
                f"Размер сообщения ({len(message)} символов) превышает вместимость "
                f"контейнера ({capacity} символов)"
            )

        try:
            message_with_marker = message + '[END]'

            binary_message = self.text_to_binary(message_with_marker)

            pixels_flat = self.pixels.reshape(-1)

            for i, bit in enumerate(binary_message):
                pixel_value = pixels_flat[i]

                masked_value = pixel_value & 0xFE

                new_value = masked_value | int(bit)

                pixels_flat[i] = new_value

            modified_pixels = pixels_flat.reshape(self.pixels.shape)

            result_image = Image.fromarray(modified_pixels.astype('uint8'), 'RGB')

            result_image.save(output_path, 'PNG')

            return True

        except Exception as e:
            raise Exception(f"Ошибка при встраивании: {str(e)}")

    def get_image_info(self):
      
        return {
            'width': self.width,
            'height': self.height,
            'size': f"{self.width}×{self.height}",
            'capacity': self.calculate_capacity(),
            'total_pixels': self.height * self.width,
            'total_bits': self.height * self.width * 3
        }


if __name__ == "__main__":
    try:

        encoder = LSBEncoder("lev1.png")
        print("Информация об изображении:", encoder.get_image_info())

        message = "Hello World"
        encoder.embed_data(message, "stego_image.png")
        print("Встраивание завершено успешно")
    except Exception as e:
        print(f"Ошибка: {e}")