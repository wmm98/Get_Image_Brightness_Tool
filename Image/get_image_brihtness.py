import numpy as np
from PIL import Image
import os


class ImageBrightness:
    def __init__(self, image_path):
        self.image_path = image_path

    def simple_rgb_average(self):
        """计算 RGB 三通道的全局算术平均亮度"""
        try:
            img = Image.open(self.image_path).convert("RGB")
            rgb_array = np.array(img)
            return np.mean(rgb_array)
        except FileNotFoundError:
            raise ValueError(f"文件不存在: {self.image_path}")
        except Exception as e:
            raise ValueError(f"图像读取失败: {str(e)}")


        

