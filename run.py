import os
from Common.config import Config
print("运行到这里")

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

def run_image_brightness():
    pass