import os
import time
import yaml
from Common.config import Config
from Image import get_brihtness
from Image import split_video


if not os.path.exists(Config.ae_result_path):
    os.mkdir(Config.ae_result_path)
if not os.path.exists(Config.ae_convergence_path):
    os.mkdir(Config.ae_convergence_path)
if not os.path.exists(Config.ae_50lux_frames_path):
    os.mkdir(Config.ae_50lux_frames_path)
if not os.path.exists(Config.ae_400lux_frames_path):
    os.mkdir(Config.ae_400lux_frames_path)
if not os.path.exists(Config.ae_1000lux_frames_path):
    os.mkdir(Config.ae_1000lux_frames_path)

def clear_directory(directory):
    if os.path.exists(directory):
        if os.listdir(directory):
            for file in os.listdir(directory):
                os.remove(os.path.join(directory, file))

def run_image_brightness():
    with open(Config.config_yaml_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    template_path = os.path.join(Config.report_template_base_path, Config.template_name)
    origin_path_path = Config.original_template_path
    if os.path.exists(template_path):
        os.remove(template_path)
    shutil.copy(Config.original_template_path, Config.report_template_base_path)

    print("运行到这里")
    cls_image_brightness = get_brihtness.ImageBrightness()
    cls_video = split_video.VideoSplitter()
    # 获取AE收敛视频文件夹路径, 将收敛视频分为一帧一帧的图片，存在ae_result/convergence/50lux、400lux、1000lux文件夹下
    ae_convergence_folder_path = data["CameraData"]["ae_convergence_folder_path"]
    for ae_cvg_video in os.listdir(ae_convergence_folder_path):
        if ae_cvg_video.find("50lux") != -1:
            clear_directory(Config.ae_50lux_frames_path)
            cls_video.extract_frames(os.path.join(ae_convergence_folder_path, ae_cvg_video), Config.ae_50lux_frames_path)
        elif ae_cvg_video.find("400lux") != -1:
            clear_directory(Config.ae_400lux_frames_path)
            cls_video.extract_frames(os.path.join(ae_convergence_folder_path, ae_cvg_video), Config.ae_400lux_frames_path)
        elif ae_cvg_video.find("1000lux") != -1:
            clear_directory(Config.ae_1000lux_frames_path)
            cls_video.extract_frames(os.path.join(ae_convergence_folder_path, ae_cvg_video), Config.ae_1000lux_frames_path)

    # 获取AE稳定性图片文件夹路径，计算亮度值
    ae_stability_folder_path = data["CameraData"]["ae_stability_folder_path"]
