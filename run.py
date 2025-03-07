import os
import time
import yaml
import shutil
from Common.config import Config
from Image import get_brihtness
from Image import split_video
from Common import get_report_position, write_report_data


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

with open(Config.first_frame_info_txt, "w+") as f:
    f.write("第一帧信息：\n")

def clear_directory(directory):
    if os.path.exists(directory):
        if os.listdir(directory):
            for file in os.listdir(directory):
                os.remove(os.path.join(directory, file))

def run_image_brightness():
    with open(Config.config_yaml_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)

    template_path = os.path.join(Config.report_template_base_path, Config.template_name)
    # print("template_path: ", template_path)
    # print("Config.original_template_path: ", Config.original_template_path)
    # print("Config.report_template_base_path: ", Config.report_template_base_path)
    if os.path.exists(template_path):
        os.remove(template_path)
        time.sleep(2)
    shutil.copy(Config.original_template_path, Config.report_template_base_path)

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
    #
    # 获取AE稳定性图片文件夹路径，计算亮度值并写入报告
    ae_stability_folder_path = data["CameraData"]["ae_stability_folder_path"]
    # 获取AE稳定性测试数据
    ae_stability_data = {}
    if os.listdir(ae_stability_folder_path):
        for ae_stability_img in os.listdir(ae_stability_folder_path):
            if ae_stability_img.find("8lux") != -1 and ae_stability_img.find("128lux") == -1:
                ae_stability_data["lux_8"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("16lux") != -1:
                ae_stability_data["lux_16"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("32lux") != -1:
                ae_stability_data["lux_32"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("64lux") != -1:
                ae_stability_data["lux_64"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("128lux") != -1:
                ae_stability_data["lux_128"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("250lux") != -1:
                ae_stability_data["lux_250"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("500lux") != -1:
                ae_stability_data["lux_500"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))
            elif ae_stability_img.find("1000lux") != -1:
                ae_stability_data["lux_1000"] = cls_image_brightness.get_simple_rgb_average(os.path.join(ae_stability_folder_path, ae_stability_img))

    # 获取A稳定性需填入数据cell的位置
    ae_stability_position = get_report_position.GetReportPosition(template_path, Config.ae_stability_sheet_name)
    as_stability_all_lux_positions = ae_stability_position.get_all_ae_stability_light_lux_position(Config.ae_stability_light_lux)
    # print("位置信息：", as_stability_all_lux_positions)
    # print("测试数据：", ae_stability_data)

    # 写入AE稳定性测试数据
    ae_stability_report = write_report_data.WriteReport(template_path, Config.ae_stability_sheet_name)
    ae_stability_report.write_ae_stability_data(as_stability_all_lux_positions, ae_stability_data)

    # 获取AE收敛3种照度数据，计算亮度值并写入报告
    # 获取收敛数据
    ae_convergence_50lux_data = []
    # 获取第一帧的位置
    if os.listdir(Config.ae_50lux_frames_path):
        ae_50lux_first_frame_index = cls_image_brightness.find_first_frame(Config.ae_50lux_frames_path)['image_index']
        ae_50lux_first_frame_name = cls_image_brightness.find_first_frame(Config.ae_50lux_frames_path)['image_name']
        with open(Config.first_frame_info_txt, "a") as f1:
            f1.write("50lux图片文件夹里检测到第一帧为： 50lux\\%s \n" % ae_50lux_first_frame_name)
        for ae_convergence_50lx_img in os.listdir(Config.ae_50lux_frames_path)[ae_50lux_first_frame_index:]:
            ae_convergence_50lux_data.append(cls_image_brightness.get_simple_rgb_average(os.path.join(Config.ae_50lux_frames_path, ae_convergence_50lx_img)))

    ae_convergence_400lux_data = []
    if os.listdir(Config.ae_400lux_frames_path):
        ae_400lux_first_frame_index = cls_image_brightness.find_first_frame(Config.ae_400lux_frames_path)['image_index']
        ae_400lux_first_frame_name = cls_image_brightness.find_first_frame(Config.ae_400lux_frames_path)['image_name']
        print("第一帧的index: ", ae_400lux_first_frame_index)
        with open(Config.first_frame_info_txt, "a") as f2:
            f2.write("400lux图片文件夹里检测到第一帧为： 400lux\\%s \n" % ae_400lux_first_frame_name)
        for ae_convergence_400lx_img in os.listdir(Config.ae_400lux_frames_path)[ae_400lux_first_frame_index:]:
            # print(ae_convergence_400lx_img)
            ae_convergence_400lux_data.append(cls_image_brightness.get_simple_rgb_average(
                os.path.join(Config.ae_400lux_frames_path, ae_convergence_400lx_img)))

    ae_convergence_1000lux_data = []
    if os.listdir(Config.ae_1000lux_frames_path):
        ae_1000lux_first_frame_index = cls_image_brightness.find_first_frame(Config.ae_1000lux_frames_path)['image_index']
        ae_1000lux_first_frame_name = cls_image_brightness.find_first_frame(Config.ae_1000lux_frames_path)['image_name']
        with open(Config.first_frame_info_txt, "a") as f1:
            f1.write("1000lux图片文件夹里检测到第一帧为： 1000lux\\%s \n" % ae_1000lux_first_frame_name)
        print("第一帧的index: ", ae_1000lux_first_frame_index)

        for ae_convergence_1000lx_img in os.listdir(Config.ae_1000lux_frames_path)[ae_1000lux_first_frame_index:]:
            # print(ae_convergence_1000lx_img)
            ae_convergence_1000lux_data.append(cls_image_brightness.get_simple_rgb_average(
                os.path.join(Config.ae_1000lux_frames_path, ae_convergence_1000lx_img)))
    # print(ae_convergence_50lux_data)
    # print(ae_convergence_1000lux_data)
    # print(ae_convergence_400lux_data)
    # 获取AE收敛需填入数据cell的位置
    ae_convergence_position = get_report_position.GetReportPosition(template_path, Config.ae_convergence_sheet_name)
    print("***************************")
    ae_convergence_50lux_positions = ae_convergence_position.get_ae_convergence_positions(Config.ae_convergence_50lx, len(ae_convergence_50lux_data))
    # print(ae_convergence_50lux_positions)
    ae_convergence_400lux_positions = ae_convergence_position.get_ae_convergence_positions(Config.ae_convergence_400lx, len(ae_convergence_400lux_data))
    # print(ae_convergence_400lux_positions)
    ae_convergence_1000lux_positions = ae_convergence_position.get_ae_convergence_positions(Config.ae_convergence_1000lx, len(ae_convergence_1000lux_data))
    # print(ae_convergence_1000lux_positions)
    # 写入数据到报告
    ae_convergence_report = write_report_data.WriteReport(template_path, Config.ae_convergence_sheet_name)
    ae_convergence_report.write_ae_convergence_data(ae_convergence_50lux_positions, ae_convergence_50lux_data)
    ae_convergence_report.write_ae_convergence_data(ae_convergence_400lux_positions, ae_convergence_400lux_data)
    ae_convergence_report.write_ae_convergence_data(ae_convergence_1000lux_positions, ae_convergence_1000lux_data)
    # 获取序列号位置，写入帧数序列号
    len_number_x_position = max(len(ae_convergence_50lux_data), len(ae_convergence_400lux_data), len(ae_convergence_1000lux_data))
    ae_convergence_number_position = ae_convergence_position.get_frame_num_position(Config.ae_convergence_50lx, len_number_x_position)
    ae_convergence_report.write_ae_convergence_number_data(ae_convergence_number_position)
    # 获取结果栏，写入结果数据
    # 获取最后需要写入的value
    result_values = {}
    result_values["calculate_result"] = "统计结果:"
    result_values["lx_50_frames_sum"] = len(ae_convergence_50lux_data)
    result_values["lx_400_frames_sum"] = len(ae_convergence_400lux_data)
    result_values["lx_1000_frames_sum"] = len(ae_convergence_1000lux_data)
    # 获取最后位置所需要的数据
    lx_last_positions = {}
    lx_last_positions["lux_50"] = ae_convergence_50lux_positions[-1]
    lx_last_positions["lux_400"] = ae_convergence_400lux_positions[-1]
    lx_last_positions["lux_1000"] = ae_convergence_1000lux_positions[-1]
    # 获取最后的位置数据
    results_statistics_positions = ae_convergence_position.get_results_statistics_position(lx_last_positions)
    # 写入最后的数据
    ae_convergence_report.write_result_data(results_statistics_positions, result_values)

    # 上边框
    num_first_position = ae_convergence_number_position[0]
    x_min_position = num_first_position[0]
    # print("x_min+position", x_min_position)
    x_max_position = num_first_position[0] + len_number_x_position
    # print("x_max+position", x_max_position)
    y_min_position = num_first_position[1]
    # print("y_min+position", y_min_position)
    y_max_position = ae_convergence_1000lux_positions[0][1]
    # print("y_max+position", y_max_position)
    ae_convergence_report.write_border(x_min_position, x_max_position, y_min_position, y_max_position)

    # 画折线图
    ae_convergence_report.writ_line_chart()
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print(data["CameraData"]["report_file_name"])


    # 复制到exe当前工作目录下
    shutil.move(template_path, os.path.join(Config.ae_result_path, data["CameraData"]["report_file_name"]))


if __name__ == '__main__':
    run_image_brightness()
