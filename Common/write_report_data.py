import time

from openpyxl import load_workbook
from Common.config import Config
from Common.get_report_position import GetReportPosition
from datetime import datetime


class WriteReport:
    def __init__(self, template_path, sheet_name):
        self.sheet_name = sheet_name
        self.template_path = template_path
        self.report_position = GetReportPosition(self.template_path, self.sheet_name)

    def write_ae_stability_data(self, position, value):
        try:
            wb = load_workbook(self.template_path)
            sheet = wb[self.sheet_name]
            for k in position:
                cell = sheet.cell(row=position[k][0], column=position[k][1])
                cell.value = value[k]
            wb.save(self.template_path)
        finally:
            wb.close()

    def write_project_name(self, camera_data):
        try:
            wb = load_workbook(self.template_path)
            sheet = wb[self.sheet_name]
            position = self.report_position.get_test_project_position(Config.r_test_project)
            r_cell = sheet.cell(row=position[0], column=position[1])
            now = datetime.now()
            if now.month < 10:
                month = "0%d" % now.month
            else:
                month = now.month
            if now.day < 10:
                day = "0%d" % now.day
            else:
                day = now.day
            self.time_info = "%d%s%s" % (now.year, month, day)
            r_cell.value = "%s-%s万摄像头(%s)-%s" % (
                camera_data["project_name"], str(camera_data["pixels"]), camera_data["camera_product"], self.time_info)
            wb.save(self.file_path)
        finally:
            wb.close()

if __name__ == '__main__':
    w_r = WriteReport(Config.template_path, Config.sheet_name)
    w_r.write_scenario_data(Config.f_data_path, Config.r_F_light)
    w_r.write_hj_data()

    # w_r = WriteReport(Config.template_path, Config.sheet_name)
    # report_position = GetReportPosition(Config.template_path, Config.sheet_name)

    # 灰阶测试
    csv = CSVTestData(Config.hj_data_path)
    hj_data = csv.get_hj_relate_data(csv.read_csv_to_matrix())
    print(hj_data)

