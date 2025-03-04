import os
import sys
import importlib.util


class Config:

    # # 调试环境
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_outside_path = project_path
    print("**********************************")
    print("project_path: ", project_path)
    print("project_outside_path: ", project_outside_path)

    # # 正式目录
    # project_path = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
    # project_outside_path = os.getcwd()
    # print("**********************************")
    # print("project_path: ", project_path)
    # print("project_outside_path: ", project_outside_path)


    # AE结果目录
    ae_result_path = os.path.join(project_outside_path, "ae_result")
    ae_convergence_path = os.path.join(ae_result_path, "convergence")
    ae_50lux_frames_path = os.path.join(ae_convergence_path, "50lux")
    ae_400lux_frames_path = os.path.join(ae_convergence_path, "400lux")
    ae_1000lux_frames_path = os.path.join(ae_convergence_path, "1000lux")

    config_yaml_path = os.path.join(project_path, "ui_config.yaml")


