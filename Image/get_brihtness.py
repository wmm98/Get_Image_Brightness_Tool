import numpy as np
from PIL import Image
import os


class ImageBrightness:
    def __init__(self):
        pass

    def get_simple_rgb_average(self, image_path):
        """计算 RGB 三通道的全局算术平均亮度"""
        try:
            img = Image.open(image_path).convert("RGB")
            rgb_array = np.array(img)
            return round(np.mean(rgb_array), 3)
        except FileNotFoundError:
            raise ValueError(f"文件不存在: {image_path}")
        except Exception as e:
            raise ValueError(f"图像读取失败: {str(e)}")


        

