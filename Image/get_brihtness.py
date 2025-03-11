import numpy as np
from PIL import Image
import os


class ImageBrightness:
    def __init__(self):
        pass

    def get_simple_rgb_average(self, image_path):
        """计算 RGB 三通道的全局算术平均亮度"""
        # try:
        #     img = Image.open(image_path).convert("RGB")
        #     rgb_array = np.array(img)
        #     return round(np.mean(rgb_array), 3)
        # except FileNotFoundError:
        #     raise ValueError(f"文件不存在: {image_path}")
        # except Exception as e:
        #     raise ValueError(f"图像读取失败: {str(e)}")

        # 打开图片并转换为 RGB 模式
        image = Image.open(image_path).convert("RGB")
        width, height = image.size

        # 计算中心 1% 区域的尺寸
        crop_width, crop_height = int(width * 0.1), int(height * 0.1)
        left, top = (width - crop_width) // 2, (height - crop_height) // 2
        right, bottom = left + crop_width, top + crop_height

        # 裁剪图片中心 1% 区域
        cropped_image = image.crop((left, top, right, bottom))

        # 转换为 NumPy 数组
        pixels = np.array(cropped_image)  # 形状 (H, W, 3)

        # 计算 RGB 总均值
        total_mean = round(np.mean(pixels), 3)  # 直接对整个 RGB 数组取均值

        return total_mean

    def calculate_image_difference(self, image1, image2, use_grayscale=True):
        print(image1)
        """
        计算两张图片的差异程度。
        - use_grayscale=True：使用感知亮度计算（更符合人眼视觉）
        - use_grayscale=False：使用 RGB 直接差异计算
        """
        # img1 = np.array(image1)
        # img2 = np.array(image2)
        #
        # if use_grayscale:
        #     # 转换为感知亮度（更符合人眼感知的亮度变化）
        #     img1 = np.dot(img1[..., :3], [0.299, 0.587, 0.114])
        #     img2 = np.dot(img2[..., :3], [0.299, 0.587, 0.114])
        #
        # # 计算像素级绝对差异
        # diff = np.abs(img1 - img2)
        # return np.mean(diff)

        img1 = Image.open(image1).convert("RGB")
        rgb_array1 = np.array(img1)
        img1_brightness = round(np.mean(rgb_array1), 3)

        img2 = Image.open(image2).convert("RGB")
        rgb_array2 = np.array(img2)
        img2_brightness = round(np.mean(rgb_array2), 3)

        return abs(img1_brightness - img2_brightness)

    def find_first_frame(self, image_folder, threshold=20, use_grayscale=True):
        """
        遍历文件夹中的图片，找到第一张发生明显变化的帧。
        - threshold: 变化阈值（建议 30~100 之间，值越小越敏感）
        - use_grayscale: 是否使用感知亮度计算变化
        """
        # 获取文件夹中的所有图片，并按文件名排序
        image_files = os.listdir(image_folder)
        if not image_files:
            raise ValueError("❌ 该文件夹内没有找到图片，请检查路径是否正确！")

        first_frame = None

        # 读取第一张图片作为基准
        first_image_path = os.path.join(image_folder, image_files[0])
        previous_image = Image.open(first_image_path).convert("RGB")
        width, height = previous_image.size

        for i in range(1, len(image_files)):
            # 读取当前图片
            current_image_path = os.path.join(image_folder, image_files[i])
            current_image = Image.open(current_image_path).convert("RGB")

            # 确保所有图片尺寸一致
            current_image = current_image.resize((width, height))

            # 计算两帧之间的变化
            diff = self.calculate_image_difference(first_image_path, current_image_path, use_grayscale)
            # diff = self.calculate_image_difference(previous_image, current_image, use_grayscale)
            # diff = abs(previous_image - current_image)

            print(f"✅计算 {image_files[i]} 与第一帧的变化量：{diff:.2f}")

            if diff > threshold:
                first_frame = image_files[i]
                print(f"🎯 发现变化帧：{first_frame} (变化量 {diff:.2f} > 阈值 {threshold})")
                # 返回照片名称，照片的索引
                return {"image_name": first_frame, "image_index": i}

            # previous_image = current_image
            # first_image_path = current_image_path

        if first_frame is None:
            raise ValueError("⚠️没有检测到明显变化的帧，请降低 threshold 阈值后重试。")

    def find_diff_stability_data(self, data):
        stable_data = []
        current_list = []

        for i in range(len(data) - 1):
            if abs(data[i] - data[i + 1]) < 3:
                current_list.append({"index": i})
            else:
                if current_list:
                    # current_list.append(data[i])
                    current_list.append({"index": i})
                    stable_data.append(current_list)
                    current_list = []
        if current_list:
            # current_list.append(data[-1])
            current_list.append({"index": i + 1})
            stable_data.append(current_list)
        if stable_data:
            return stable_data

    def get_longest_sublist(self, data):
        # data：[[{1: 3}, {2: 3}], [{4: 3}, {6: 3}]]
        max_length = 0
        max_index = -1
        longest_sublist = []

        for i, sublist in enumerate(data):
            if len(sublist) >= max_length:
                max_length = len(sublist)
                max_index = i
                longest_sublist = sublist
        return longest_sublist




# if __name__ == '__main__':
#     image_br = ImageBrightness()
#
#     base_path = os.path.dirname(os.getcwd())
#
#     print(base_path)
#     # for i in os.listdir(os.path.join(base_path, "ae_result\\convergence\\50lux")):
#     #     print(i)
#     img_index = image_br.find_first_frame(os.path.join(base_path, "ae_result\\convergence\\50lux"))
#     print(img_index)

