import cv2
import os

class VideoSplitter:
    def __init__(self):
        pass

    def extract_frames(self, video_path, output_folder):
        # 创建输出文件夹（如果不存在）
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 打开视频文件
        cap = cv2.VideoCapture(video_path)

        # 检查视频是否成功打开
        if not cap.isOpened():
            raise ValueError(f"无法打开视频文件: {video_path}")

        frame_count = 0
        while True:
            # 读取一帧
            ret, frame = cap.read()

            # 如果帧读取失败，退出循环
            if not ret:
                break

            # 保存帧为图像文件
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)

            frame_count += 1

        # 释放视频捕获对象
        cap.release()
        print(f"提取了 {frame_count} 帧到文件夹: {output_folder}")