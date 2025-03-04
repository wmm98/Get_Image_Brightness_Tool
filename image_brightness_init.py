import os
import yaml
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox, QLineEdit, QCompleter, QComboBox, QButtonGroup
import sys

from Common import config

conf = config.Config()


class Image_Brightness_UI(object):
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly

    with open(conf.config_yaml_path, 'r', encoding="utf-8") as file:
        yml_data = yaml.safe_load(file)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")


        self.ae_stability_folder_info = QtWidgets.QLabel("上传AE稳定性图片（文件夹）：")
        self.verticalLayout.addWidget(self.ae_stability_folder_info)
        ae_stability_upload_folder_layout = QHBoxLayout()
        self.ae_stability_folder_path_edit = QtWidgets.QLineEdit()

        ae_stability_upload_folder_layout.addWidget(self.ae_stability_folder_path_edit)
        self.ae_stability_folder_upload_button = QtWidgets.QPushButton("点击上传")
        ae_stability_upload_folder_layout.addWidget(self.ae_stability_folder_upload_button)
        self.verticalLayout.addLayout(ae_stability_upload_folder_layout)
        self.verticalLayout.addWidget(QtWidgets.QLabel())

        # 上传AE收敛视频，可同时上传多个视频，所有的视频格式都可，不是上传文件夹，是视频文件
        self.ae_convergence_video_info = QtWidgets.QLabel("上传AE收敛视频（文件夹），视频以包含“50lux、400lux、1000lux”字符串命名：")
        self.verticalLayout.addWidget(self.ae_convergence_video_info)
        ae_convergence_upload_folder_layout = QHBoxLayout()
        self.ae_convergence_folder_path_edit = QtWidgets.QLineEdit()
        ae_convergence_upload_folder_layout.addWidget(self.ae_convergence_folder_path_edit)
        self.ae_convergence_folder_upload_button = QtWidgets.QPushButton("点击上传")
        ae_convergence_upload_folder_layout.addWidget(self.ae_convergence_folder_upload_button)
        self.verticalLayout.addLayout(ae_convergence_upload_folder_layout)
        self.verticalLayout.addWidget(QtWidgets.QLabel())

        # 设备型号
        self.device_model_layout = QHBoxLayout()
        self.device_model_info = QtWidgets.QLabel("请填写设备型号：")
        self.device_model_name = QLineEdit()
        self.device_model_layout.addWidget(self.device_model_info)
        self.device_model_layout.addWidget(self.device_model_name)
        self.device_model_layout.addStretch(1)
        self.verticalLayout.addLayout(self.device_model_layout)
        self.verticalLayout.addWidget(QtWidgets.QLabel())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 提交按钮
        self.submit_button = QtWidgets.QPushButton("开始生成报告")
        self.verticalLayout.addWidget(self.submit_button)

        self.tips = QtWidgets.QLabel()
        self.tips.setStyleSheet("color: red;")
        self.tips.setText("未开始生成报告...")
        # self.tips.setVisible(False)
        self.verticalLayout.addWidget(self.tips)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "获取图片RGB亮度值工具"))
