# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from Common.config import Config
from image_brightness_init import Image_Brightness_UI
import yaml
import os
import shutil
from datetime import datetime
from run import run_image_brightness

import numpy as np
from PIL import Image
import cv2
from openpyxl import load_workbook
from Common.get_report_position import GetReportPosition
from openpyxl.styles import Alignment, Border, Side, PatternFill
from openpyxl.chart import LineChart, Reference


class ScriptThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        run_image_brightness()
        self.finished.emit()


class Image(QtWidgets.QMainWindow, Image_Brightness_UI):
    def __init__(self):
        super(Image, self).__init__()
        self.setupUi(self)
        self.intiui()
        self.final_report_name = ""
        self.err_flag = 0

    def intiui(self):
        self.ae_stability_folder_upload_button.clicked.connect(self.upload_ae_stability_folder)
        self.ae_convergence_folder_upload_button.clicked.connect(self.upload_ae_convergence_folder)
        self.submit_button.clicked.connect(self.handle_submit)

    def get_message_box(self, text):
        QMessageBox.warning(self, "错误提示", text)

    def handle_submit(self):
        if not self.ae_stability_folder_path_edit.text():
            self.get_message_box("请上传AE稳定性图片文件夹!!!")
            return
        if not os.path.exists(self.ae_stability_folder_path_edit.text()):
            self.get_message_box("AE稳定性图片文件夹不存在!!!")

        if not self.ae_convergence_folder_path_edit.text():
            self.get_message_box("请上传AE收敛视频文件夹")
            return
        if not os.path.exists(self.ae_convergence_folder_path_edit.text()):
            self.get_message_box("AE收敛视频文件夹不存在!!!")
            return

        if not self.device_model_name.text():
            self.get_message_box("请填写设备型号")
            return
        # 保存设备信号信息到yaml文件
        self.yml_data["CameraData"]["device_model_name"] = self.device_model_name.text()
        self.yml_data["CameraData"]["ae_stability_folder_path"] = self.ae_stability_folder_path_edit.text()
        self.yml_data["CameraData"]["ae_convergence_folder_path"] = self.ae_convergence_folder_path_edit.text()

        now = datetime.now()
        if now.month < 10:
            month = "0%d" % now.month
        else:
            month = now.month
        if now.day < 10:
            day = "0%d" % now.day
        else:
            day = now.day
        # 时间精确到S
        time_info = "%d%s%s-%s_%s_%s" % (now.year, month, day, now.hour, now.minute, now.second)
        self.final_report_name = "%s-RGB图像测试报告-%s.xlsx" % (self.yml_data["CameraData"]["device_model_name"], time_info)
        self.yml_data["CameraData"]["report_file_name"] = self.final_report_name
        # while True:
        #     if self.path_is_existed(os.path.join(Config.ae_result_path, self.final_report_name)):
        #         print("报告已经存在")
        #         self.err_flag += 1
        #     else:
        #         if self.err_flag > 0:
        #             self.final_report_name = "%s-RGB图像测试报告-%s-(%d).xlsx" % (self.yml_data["CameraData"]["device_model_name"], time_info, self.err_flag)
        #         else:
        #             self.final_report_name = "%s-RGB图像测试报告-%s.xlsx" % (self.yml_data["CameraData"]["device_model_name"], time_info)
        #         break
        #     time.sleep(0.2)
        self.yml_data["CameraData"]["report_err_flag"] = self.err_flag
        self.yml_data["CameraData"]["report_file_name"] = self.final_report_name
        # # 保存修改后的内容回 YAML 文件
        with open(Config.config_yaml_path, 'w') as file:
            yaml.safe_dump(self.yml_data, file)
        print("##########################################")
        print(self.final_report_name)

        # # 显示报告正在生成中
        self.tips.setText("正在生成报告,请等待.....")
        # # 单独线程运行,避免阻塞主线程和 PyQt5 的事件
        #
        self.script_thread = ScriptThread()
        self.script_thread.finished.connect(self.thread_finish)
        self.script_thread.start()
        #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_report)
        print("开始计时生成报告")
        #
        self.check_interval = 1000  # 定时器间隔，单位毫秒
        self.timeout_limit = 60 * 1000  # 超时限制，单位毫秒, 10秒超时
        self.elapsed_time = 0  # 已经过的时间
        #
        self.timer.start(self.check_interval)  # 启动定时器

    def recover_yaml_data(self):
        with open(Config.config_yaml_path, 'r') as file:
            re_yml_data = yaml.safe_load(file)

        re_yml_data["CameraData"]["device_model_name"] = ''
        re_yml_data["CameraData"]["ae_stability_folder_path"] = ''
        re_yml_data["CameraData"]["ae_convergence_folder_path"] = ''
        re_yml_data["CameraData"]["report_err_flag"] = ''
        re_yml_data["CameraData"]["report_file_name"] = ''

        with open(Config.config_yaml_path, 'w') as file:
            yaml.safe_dump(re_yml_data, file)

    def thread_finish(self):
        path = os.path.join(Config.ae_result_path, self.final_report_name)  # 要检查的路径
        if not os.path.exists(path):
            self.tips.setText("生成报告失败,请再次生成")
            self.timer.stop()
            self.recover_yaml_data()
    #
    def check_report(self):
        path = os.path.join(Config.ae_result_path, self.final_report_name)  # 要检查的路径
        if os.path.exists(path):
            self.tips.setText("报告已经生成:  %s" % self.final_report_name)
            self.timer.stop()  # 如果报告存在，停止定时器
        else:
            self.elapsed_time += self.check_interval
            if self.elapsed_time >= self.timeout_limit:
                self.tips.setText("生成报告失败,请再次生成")
                self.timer.stop()  # 如果超时，停止定时器

    def closeEvent(self, event):
        self.timer.stop()  # 在窗口关闭时停止定时器
        self.recover_yaml_data()
        event.accept()

    def check_file_extension_name(self, file_name, light):
        if ".csv" != os.path.splitext(file_name)[1].strip():
            self.get_message_box("%s光数据请上传csv格式的数据!!!" % light)
            return False
        return True

    def deal_csv_file(self, light, file_path):
        if light == "JXL":
            csv_name = light + "_Y_multi" + os.path.splitext(file_path)[1]
        else:
            csv_name = light + "_summary" + os.path.splitext(file_path)[1]
        # test_data_path = os.path.join(self.project_path, "TestData")
        des_folder = os.path.join(self.test_data_path, light)
        des_file = os.path.join(des_folder, csv_name)
        file_copied_path = os.path.join(des_folder, os.path.basename(file_path))
        self.remove_file(des_file)
        self.remove_file(des_file)
        self.copy_file(file_path, des_folder)
        if not self.path_is_existed(des_file):
            self.copy_file(file_path, des_folder)
        self.rename_file(file_copied_path, des_file)

    def copy_file(self, origin, des):
        shutil.copy(origin, des)

    def rename_file(self, origin, des):
        shutil.move(origin, des)

    def remove_file(self, path):
        if os.path.isfile(path):
            os.remove(path)

    def path_is_existed(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def upload_ae_stability_folder(self):
        ae_stability_folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if ae_stability_folder_path:
            self.ae_stability_folder_path_edit.setText(ae_stability_folder_path)

    def upload_ae_convergence_folder(self):
        ae_convergence_folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if ae_convergence_folder_path:
            self.ae_convergence_folder_path_edit.setText(ae_convergence_folder_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Image()
    myshow.show()
    sys.exit(app.exec_())
