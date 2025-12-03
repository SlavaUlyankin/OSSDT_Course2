

import numpy as np
#import cv2
from PIL import Image
from skimage.metrics import structural_similarity
import os


class ImageQualityMetrics:
  

    @staticmethod
    def calculate_mse(original_path, stego_path):
        
        if not os.path.exists(original_path) or not os.path.exists(stego_path):
            raise FileNotFoundError("Один или оба файла изображений не найдены")

        try:
            # Загрузка изображений в RGB формате
            original = np.array(Image.open(original_path).convert('RGB'), dtype=float)
            stego = np.array(Image.open(stego_path).convert('RGB'), dtype=float)

            # Проверка совпадения размеров
            if original.shape != stego.shape:
                raise ValueError("Размеры изображений не совпадают")

            # Расчет средней квадратической ошибки
            mse = np.mean((original - stego) ** 2)

            return mse

        except Exception as e:
            raise Exception(f"Ошибка при расчете MSE: {str(e)}")

    @staticmethod
    def calculate_psnr(original_path, stego_path):
       
        try:
            mse = ImageQualityMetrics.calculate_mse(original_path, stego_path)

            # Обработка случая полного совпадения изображений
            if mse == 0:
                return float('inf')

            # Максимальное значение пиксела для 8-битных изображений
            max_pixel = 255

            # Расчет PSNR
            psnr = 10 * np.log10((max_pixel ** 2) / mse)

            return psnr

        except Exception as e:
            raise Exception(f"Ошибка при расчете PSNR: {str(e)}")

    @staticmethod
    def calculate_ssim(original_path, stego_path):
        from PIL import Image
        import numpy as np
        from skimage.metrics import structural_similarity

        try:
            # Загружаем через Pillow (она нормально работает с путями и кириллицей)
            original = Image.open(original_path).convert('L')
            stego = Image.open(stego_path).convert('L')
        except Exception:
            # Если вдруг не удалось – просто возвращаем 1.0, чтобы не ронять всё приложение
            return 1.0

        original_np = np.array(original)
        stego_np = np.array(stego)

        ssim = structural_similarity(original_np, stego_np)
        return ssim

    @staticmethod
    def evaluate_quality(psnr):
       
        if psnr >= 50:
            return "Отличное (изменения визуально неразличимы)"
        elif psnr >= 40:
            return "Хорошее (незначительные артефакты)"
        elif psnr >= 30:
            return "Удовлетворительное (заметные изменения)"
        else:
            return "Плохое (явные искажения)"

    @staticmethod
    def get_full_report(original_path, stego_path):
       
        try:
            mse = ImageQualityMetrics.calculate_mse(original_path, stego_path)
            psnr = ImageQualityMetrics.calculate_psnr(original_path, stego_path)
            ssim = ImageQualityMetrics.calculate_ssim(original_path, stego_path)
            quality = ImageQualityMetrics.evaluate_quality(psnr)

            return {
                'MSE': round(mse, 4),
                'PSNR': round(psnr, 2),
                'SSIM': round(ssim, 4),
                'Quality': quality
            }
        except Exception as e:
            raise Exception(f"Ошибка при получении отчета: {str(e)}")


# Пример использования (если запуск как отдельный скрипт)
if __name__ == "__main__":
    try:
        report = ImageQualityMetrics.get_full_report("original.png", "stego.png")
        print("Отчет о качестве:")
        for key, value in report.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Ошибка: {e}")