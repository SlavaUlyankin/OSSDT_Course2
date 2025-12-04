import unittest
import os
import numpy as np
from PIL import Image
from lsb_encoder import LSBEncoder
from lsb_decoder import LSBDecoder
from metrics import ImageQualityMetrics

class TestLSBSteganography(unittest.TestCase):
    
    def setUp(self):
        #"""Подготовка окружения перед каждым тестом"""
        # Создаем тестовое изображение 50x50 пикселей (красный цвет)
        self.test_image_name = "test_base.png"
        self.stego_image_name = "test_stego.png"
        self.width = 50
        self.height = 50
        
        image = Image.new('RGB', (self.width, self.height), color='red')
        image.save(self.test_image_name)
        
        self.encoder = LSBEncoder(self.test_image_name)
        self.message = "Test Message 123"

    def tearDown(self):
        #"""Очистка после тестов (удаление временных файлов)"""
        if os.path.exists(self.test_image_name):
            os.remove(self.test_image_name)
        if os.path.exists(self.stego_image_name):
            os.remove(self.stego_image_name)

    def test_text_to_binary_conversion(self):
        #"""Тест конвертации текста в бинарный вид и обратно"""
        text = "Abc"
        # 'A' = 65 = 01000001
        expected_binary_start = "01000001"
        
        binary = self.encoder.text_to_binary(text)
        self.assertTrue(binary.startswith(expected_binary_start))
        
        # Проверка обратной конвертации
        recovered_text = self.encoder.binary_to_text(binary)
        self.assertEqual(text, recovered_text)

    def test_calculate_capacity(self):
        #"""Тест расчета вместимости контейнера"""
        # 50 * 50 пикселей * 3 канала = 7500 бит
        # 7500 // 8 = 937 байт
        # Вместимость = 937 - 10 (резерв) = 927
        capacity = self.encoder.calculate_capacity()
        self.assertEqual(capacity, 927)

    def test_embedding_and_extraction(self):
        #"""Интеграционный тест: встраивание и последующее извлечение"""
        # 1. Встраиваем сообщение
        self.encoder.embed_data(self.message, self.stego_image_name)
        
        # 2. Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.stego_image_name))
        
        # 3. Извлекаем сообщение
        decoder = LSBDecoder(self.stego_image_name)
        extracted_message = decoder.extract_data()
        
        self.assertEqual(self.message, extracted_message)

    def test_overflow_protection(self):
        #"""Тест защиты от переполнения контейнера"""
        huge_message = "A" * 2000 # Сообщение больше вместимости (927 байт)
        with self.assertRaises(ValueError):
            self.encoder.embed_data(huge_message, self.stego_image_name)

    def test_metrics_calculation(self):
        #"""Тест расчета метрик качества"""
        # Создаем копию изображения 
        self.encoder.image.save(self.stego_image_name)
    
        psnr = ImageQualityMetrics.calculate_psnr(self.test_image_name, self.stego_image_name)
        self.assertEqual(psnr, float('inf'))
        
        mse = ImageQualityMetrics.calculate_mse(self.test_image_name, self.stego_image_name)
        self.assertEqual(mse, 0.0)

if __name__ == '__main__':
    unittest.main()
